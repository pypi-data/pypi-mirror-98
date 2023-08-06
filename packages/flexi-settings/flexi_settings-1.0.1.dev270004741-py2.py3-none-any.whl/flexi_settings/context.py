"""The context for :class:`ServiceSettings <base_settings.ServiceSettings>`."""

import os
from dataclasses import dataclass
from typing import List


@dataclass
class SettingsContext(object):
    """Context with customized configuration.

    These values may be defined directly via the constructor. When creating the context via
    the :class:`SettingsContextSingleton`, the values may also be defined via environ variables
    as listed for each.

    **Environment Variables**

    This library looks for environ vars with the prefix of "VR\\_".

    ================ ==============
    Name             Description
    ================ ==============
    VR_PREFIX        Your service's standard variable prefix (i.e., "MSX\\_")
    VR_SERVICE_NAME  The service name label
    VR_SETTINGS_NAME The filename of the primary settings file
    VR_SETTINGS_DIR  The default directory to find settings files
    VR_OVERRIDE      The filename of the optional local override file
    ================ ==============

    """

    service_name: str
    """The service name. Used to default ``settings_root_dir``."""

    var_prefix: str = None
    """Prefix for environ vars and other names. Set to the prefix with or without trailing '_'."""

    settings_root_dir: str = None
    """Default directory containing settings file(s). Define with: VR_SETTINGS_DIR"""

    settings_filename: str = "settings.yml"
    """The default filename for the primary settings. Define with: VR_SETTINGS_NAME"""

    overload_filename: str = None
    """Optional settings overload filename"""

    docker_configs_dir: str = None
    """To support resolving from Docker configs set this to the configs directory"""

    docker_secrets_dir: str = None
    """To support resolving from Docker secrets set this to the secrets dir (/run/secret)"""

    resolvers: List[str] = None
    """Optional list of (additional) resolver names to support"""

    def __post_init__(self):
        """For applying post-init values to self."""
        self._apply_env_vars()
        self._apply_adjustments()

    def _apply_adjustments(self):
        """Adjust settings for consistency as expected."""
        self.settings_root_dir = self.settings_root_dir or "/etc/{}".format(self.service_name)

        if self.var_prefix and not self.var_prefix.endswith("_"):
            self.var_prefix += "_"

    def _apply_env_vars(self):
        """To optionally apply values from environment vars prefixed with 'VR\\_'"""
        # These use internal over environment
        self.service_name = self.service_name or os.environ.get('VR_SERVICE_NAME')
        self.var_prefix = self.var_prefix or os.environ.get('VR_PREFIX')
        # These use environment over internal
        self.settings_root_dir = os.environ.get('VR_SETTINGS_DIR') or self.settings_root_dir
        self.settings_filename = os.environ.get('VR_SETTINGS_NAME') or self.settings_filename
        self.overload_filename = os.environ.get('VR_OVERRIDE') or self.overload_filename

        # TODO: Use an EnvVarResolver to get/resolve values

    def enable_docker_secrets(self, root_dir: str = None):
        """Enable the :class:`DockerSecretsResolver <docker_resolver.DockerSecretsResolver>` support.

        :param root_dir: Optional, alternate directory. Defaults to "/run/secrets"
        """
        self.docker_secrets_dir = root_dir or "/run/secrets"

    def enable_docker_configs(self, root_dir: str = None):
        """Enable the :class:`DockerSecretsResolver <docker_resolver.DockerSecretsResolver>` support.

        :param root_dir: Optional, alternate directory. Defaults to "/"
        """
        self.docker_configs_dir = root_dir or "/"

    def get_settings_filename(self) -> str:
        """Get the primary settings filename from self."""
        return os.path.realpath(os.path.join(self.settings_root_dir, self.settings_filename))


class SettingsContextSingleton(object):
    """A singleton for maintaining a "global" context instance."""

    _instance: SettingsContext = None
    """Singleton :class:`SettingsContext` instance."""

    envvar_prefix = "VR_PREFIX"
    """To define the service environ and other vars prefix (i.e., 'VR\\_')"""

    _settings_root_dir = "VR_SETTINGS_DIR"
    """Directory settings are found"""

    envvar_settings_filename = "VR_SETTINGS_NAME"
    """Primary settings file name"""

    envvar_overload_filename = "VR_OVERLOAD_NAME"
    """Optional local settings overload filename"""

    envvar_service_name = "VR_SERVICE_NAME"

    def __init__(self):
        pass

    @classmethod
    def reset(cls, context: SettingsContext = None):
        """Reset the global context to None or a specific value"""
        cls._instance = context

    @classmethod
    def instance(cls, context: SettingsContext = None) -> SettingsContext:
        """Get or create :class:`SettingsContext` instance.

        :param context: Optional context to use if there is currently no singleton instance
        :return: A :class:`SettingsContext` instance
        """
        if context:
            cls._instance = context

        if not cls._instance:
            cls._instance = cls.create_instance()

        return cls._instance

    @classmethod
    def get_instance(cls) -> SettingsContext:
        """Get the current global instance.

        :meta private:
        :return:
        """

    @classmethod
    def create_instance(cls):
        """Create instance of the :class:`SettingsContext`.

        This will inspect the "VR\\_" environ vars looking for variables to set to the new
        context.

        """
        name = os.environ.get(cls.envvar_service_name)

        _tmp = SettingsContext(service_name=name)  # To obtain the hard-coded defaults

        return SettingsContext(
            service_name=name,
            var_prefix=os.environ.get(cls.envvar_prefix) or _tmp.var_prefix,
            settings_root_dir=os.environ.get(cls._settings_root_dir) or _tmp.settings_root_dir,
            settings_filename=os.environ.get(cls.envvar_settings_filename) or _tmp.settings_filename
        )
