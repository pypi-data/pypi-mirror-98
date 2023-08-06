"""Base and supporting classes for Resolvers."""
from dataclasses import dataclass
from typing import Any, Union

from flexi_settings import BaseError
from flexi_settings.context import SettingsContextSingleton, SettingsContext
from flexi_settings.tree_data import TreeData
from flexi_settings.variable import Variable


class NotResolvedError(BaseError):
    """Resolver can not resolve the variable name."""

    def __init__(self, message: str = '', name: str = ''):
        """Construct.

        :param message: Optional full message
        :param name: Optional name of var not found
        """
        super().__init__(message='Not found: {}'.format(name) if name and not message else message)


@dataclass
class Resolution(object):
    """Contains the results from :meth:`Resolver.resolve`.

    The ``__post_init__`` will inspect the value and set the
    ``contains_vars`` flag. If ``value`` is changed directly, call the
    :meth:`has_vars` method to check if ``value`` has variables.

    """

    value: Any
    """The resolved value (which could also be a variable template)"""

    contains_vars: bool = False
    """True if the resolution contains embedded variables"""

    def has_vars(self) -> bool:
        """Called by ``__post_init__`` to check to see if ``value`` contains var templates."""
        from flexi_settings.visitors import HasVariablesVisitor, TreeDataVisitor
        from flexi_settings.variable import VariableString

        if isinstance(self.value, str):
            self.contains_vars = VariableString.str_has_vars(string=self.value)

        elif TreeDataVisitor.is_array_like(obj=self.value, tuple_is_array=True):
            self.contains_vars = HasVariablesVisitor().check(node=self.value)

        return self.contains_vars

    def __post_init__(self):
        self.has_vars()

    def __eq__(self, o: object) -> bool:
        """Compare a scalar to self.value"""
        if isinstance(o, Resolution):
            return super().__eq__(o)

        return o == self.value


class Resolver(object):
    """Base class for both built-in and custom resolvers.

    Implementations must implement the :meth:`resolve` method and optionally
    the :meth:`discover` method.

    """

    def __init__(self, name: str, settings_context: SettingsContext = None):
        """Construct.

        :param name:
        :param settings_context:
        """
        self.name = name

        self._content: TreeData = None
        """Holder for the loaded/discovered data"""

        self.settings_context = settings_context or SettingsContextSingleton.instance()
        """Settings referenced by (some) resolvers."""

    @property
    def content(self) -> TreeData:
        """To fetch the contents loaded."""
        return self._content

    @content.setter
    def content(self, data: TreeData):
        """Set the contents."""
        self._content = data

    def set_content(self, data: TreeData = None, dict_vars: dict = None):
        """Set content from either a :class:`TreeData <tree_data.TreeData>` or ``dict``."""
        if data:
            self._content = data
        elif dict_vars is not None:
            self._content = TreeData(**dict_vars)
        else:
            self._content = TreeData()

    def get_root_var_name(self, name_with_prefix: str):
        """Get just the var name with the prefix stripped off.

        This references the :class:`SettingsContext.var_prefix <context.SettingsContext>`
        for the standard prefix. If ``name_with_prefix`` does not have the
        prefix it is simply returned as-is.

        :param name_with_prefix: A variable name possibly with the standard prefix
        """
        return name_with_prefix.replace(self.settings_context.var_prefix, "")

    def get_prefix_var_name(self, name: str, toupper: bool = False):
        """Get the variable name with the standard prefix.

        This returns ``name`` if the variable already has the prefix.

        :param name: Name with or without the standard prefix
        :param toupper: True to also return ``name`` as upper case
        :return: Name with the standard prefix
        """
        if toupper:
            name = name.upper()

        if name.startswith(self.settings_context.var_prefix):
            return name

        return '{}{}'.format(self.settings_context.var_prefix, name)

    def toggle_name_prefix(self, name: str) -> str:
        """Toggle the name to include/exclude the prefix.

        .. code-block: python

            self.toggle_name_prefix("MSX_NAME")  # "NAME"
            self.toggle_name_prefix("NAME")  # "MSX_NAME"

        """
        if name.startswith(self.settings_context.var_prefix):
            return self.get_root_var_name(name_with_prefix=name)

        return self.get_prefix_var_name(name=name)

    # noinspection PyMethodMayBeStatic
    def discover(self) -> Union[TreeData, None]:
        """Optional method to discover content on creating instance.

        This will "load" the data into :meth:`content` property.

        :return: The loaded :class:`TreeData <tree_data.TreeData>` (same as :meth:`content` returns)
        """
        return None

    def resolve(self, variable: Union[Variable, str], safe: bool = False) -> Union[Resolution, None]:
        """Resolve a variable by name/variable reference.

        To ensure that ``variable`` is of type :class:`Variable <variable.Variable>` use
        the :func:`to_variable <flexi_settings.to_variable>` decorator.

        This should be an "on-demand" function that will resolve from the "current"
        values. For static content (like YAML/JSON files) it will resolve from
        the content loaded when the Resolver is created. For resolvers that
        are tied to content such as environ variables or Docker swarm config/secret
        files, it must inspect the content on-demand to pick up the current content.

        If the resolver can not resolve the variable it should raise
        a :class:`NotResolvedError` exception.

        .. note::

            Resolver classes must implement this method.

        :param variable: Source to match. May be a ``str`` or ``Variable`` (preferred).
        :param safe: True to return None if not resolved rather than raising :class:`NotResolvedError`
        :return: A Resolution object
        :raises NotResolvedError: If the resolver does not find the variable.
        """
        raise NotImplementedError()
