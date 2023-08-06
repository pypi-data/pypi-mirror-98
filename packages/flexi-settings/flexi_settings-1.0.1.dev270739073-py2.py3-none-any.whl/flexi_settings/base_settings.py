"""Helper base class to manage overall settings.

This may be used or extended to provide access to dynamic settings within a service.
"""
from __future__ import annotations
import os
import threading
from typing import Any, Union, Tuple, Optional
import pathlib as pp

from flexi_settings.context import SettingsContextSingleton, SettingsContext
from flexi_settings.docker_resolver import DockerConfigsResolver, DockerSecretsResolver
from flexi_settings.override_visitor import OverrideVisitor
from flexi_settings.resolver import NotResolvedError
from flexi_settings.tree_data import TreeData, UNDEFINED_MAGIC
from flexi_settings.tree_data_resolver import TreeDataResolver
from flexi_settings.var_resolver import VariableResolver


class ServiceSettings(object):
    """Base class to manage overall service settings.

    A service will initialize a :class:`SettingsContext <context.SettingsContext>` that this
    uses to find the list of overrides/resolvers. The primary settings file is loaded, keys
    are updated from the list of resolvers, and calls to :meth:`get_field` will return
    values that are potentially overloaded via one of the resolvers.


    If ``filename`` is omitted, the filename is obtained via the ``settings_context``.
    If that is also None, the default context Singleton is used.

    .. note::

        This class may be used as-is, or extended to provide specialized features for a
        service.

    """

    _instance: ServiceSettings = None
    _lock_it = threading.RLock()

    def __init__(self,
                 filename: str = None,
                 settings_context: SettingsContext = None,
                 force_reload: bool = False
                 ):
        """Construct.

        The recommended method for obtaining a reference to settings is to use the
        singleton method :meth:`instance`.

        :param filename: The settings filename to load
        :param settings_context: A :class:`SettingsClass` or None for default
        :param force_reload: Force a reload of the settings instance
        """
        self.context = settings_context or SettingsContextSingleton.instance()
        """The :class:`context.SettingsContextSingleton` instance. If None, obtains the default."""

        self.filename = filename or self.context.get_settings_filename()
        """The filename of the primary service settings."""

        # Verify that it's present (but not yet that it's valid)
        if not os.path.exists(self.filename):
            raise FileNotFoundError(self.filename)

        self.settings: TreeData = None
        self.resolver: VariableResolver = None

        if not ServiceSettings._instance or force_reload:
            self.set_instance(self._load())

        elif ServiceSettings._instance:
            self.set_from_instance()

    @classmethod
    def instance(cls, filename: str = None,
                 settings_context: SettingsContext = None,
                 force_reload: bool = True) -> ServiceSettings:
        """Get or create :class:`ServiceSettings` instance"""
        with cls._lock_it:
            if not cls._instance:
                settings = cls(filename=filename, settings_context=settings_context, force_reload=force_reload)
                cls._instance = settings

        return cls._instance

    @classmethod
    def set_instance(cls, instance: Optional[ServiceSettings]):
        """Set the global instance.

        This is primarily *only* to support testing.

        :meta private:
        :param instance:
        :return:
        """
        with cls._lock_it:
            cls._instance = instance

    def set_from_instance(self):
        """Set self from existing class ``_instance``."""
        self.settings = self._instance.settings
        self.resolver = self._instance.resolver

    @classmethod
    def get_instance(cls):
        """Get the global instance.

        This is primarily *only* to support testing.

        :meta private:
        :return:
        """
        return cls._instance

    @classmethod
    def get(cls, field_name: str, safe: bool = False, default=UNDEFINED_MAGIC) -> Any:
        """Get field value helper from the :class:`ServiceSettings` Singleton."""
        if not cls._instance:
            raise ValueError('The ServiceSettings is not yet initialized')

        return cls._instance.get_field(field_name=field_name, safe=safe, default=default)

    def get_field(self, field_name: str, safe: bool = False, default=UNDEFINED_MAGIC) -> Any:
        """Get field value with optional auto-decryption.

        If `auto_decrypt` is True and the field is encoded as encrypted, this will auto decrypt
        it before returning.

        .. note::

            The plaintext value should **not** be retained longer than required for security reasons.

        If the ``safe`` parameter is True this will return None if the field is not found. If it
        is False, this raises a :class:`NotResolvedError <resolver.NotResolvedError>` exception.

        :param field_name: The key to get.
        :param default: Optional default value if not found, including None.
        :param safe: True to return None if field is not found
        :return:
        :raises NotResolvedError: If the ``field_name`` key is not found
        """
        try:
            value = self.resolver.get_field(string=field_name, recursive=True, default=default)
            return value

        except NotResolvedError:
            if safe:
                return None
            raise NotResolvedError('Failed to resolve field_name: {}'.format(field_name))

    def update_string(self, str_with_fields: str) -> str:
        """To resolve variables within a string.

        .. code-block:: python

            settings.get_field("This will resolve !FIELD_VAR!")

        :param str_with_fields: A ``str`` with embedded fields
        :return: String with fields replaced with values
        """
        string = self.resolver.resolve_string(string=str_with_fields)

        return string

    def update_dict(self, dict_with_fields: dict) -> dict:
        """Update dict values, replacing fields with resolved values.

        The dict values may be either scalar or dict/list items.

        :param dict_with_fields:
        :return:
        :raises NotResolvedError: If one or more fields are not resolved
        """
        return self.resolver.visit(dict_with_fields)

    def update_list(self, list_with_fields: str) -> list:
        """Update list items, replacing fields with resolved values.

        The list items may be either scalar strings or dict/list items.

        :param list_with_fields: List with items containing fields
        :return:
        :raises NotResolvedError: If one or more fields are not resolved
        """

    def _load(self) -> ServiceSettings:
        """Load and blend the settings."""
        from flexi_settings.env_resolver import EnvVarResolver

        settings_resolver = TreeDataResolver(filename=self.filename)
        self.settings = settings_resolver.content

        env_resolver = EnvVarResolver()
        override_resolver = self._get_override_resolver()
        configs_resolver, secrets_resolver = self._get_docker_resolvers()

        resolvers = [r for r in [override_resolver, env_resolver, configs_resolver, secrets_resolver, settings_resolver] if r]
        overrides = [item.content for item in resolvers]

        # Given the loaded settings, apply overrides
        visitor = OverrideVisitor(overrides=overrides)
        visitor.visit(node=self.settings)

        self.resolver = VariableResolver(resolvers=resolvers)

        return self

    def _get_override_resolver(self) -> Union[TreeDataResolver, None]:
        """If specified, and present, load the override file.

        :return: A :class:`TreeDataResolver <tree_data_resolver.TreeDataResolver>` or None if not present
        """
        if self.context.overload_filename:
            name = pp.PurePath(self.context.overload_filename)
            if not name.anchor:
                name = pp.PurePath(self.context.settings_root_dir, self.context.overload_filename)

            if os.path.exists(name):
                return TreeDataResolver(filename=str(name))

        return None

    def _get_docker_resolvers(self) -> Tuple[DockerConfigsResolver, DockerSecretsResolver]:
        configs = DockerConfigsResolver(root_dir=self.context.docker_configs_dir) if self.context.docker_configs_dir else None
        secrets = DockerSecretsResolver(root_dir=self.context.docker_secrets_dir) if self.context.docker_secrets_dir else None

        return configs, secrets
