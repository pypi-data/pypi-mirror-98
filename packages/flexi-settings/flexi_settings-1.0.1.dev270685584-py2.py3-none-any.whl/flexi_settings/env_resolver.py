"""For resolving variables from environ variables."""
import os
from typing import Union

from flexi_settings import to_variable
from flexi_settings.context import SettingsContext
from flexi_settings.resolver import Resolver, Resolution, NotResolvedError
from flexi_settings.tree_data import TreeData
from flexi_settings.variable import Variable


class EnvVarResolver(Resolver):
    """Resolve from environment variables."""

    def __init__(self, name: str = None, settings_context: SettingsContext = None):
        super().__init__(name or 'envvar_resolver', settings_context=settings_context)

        self.content = self.discover()

    def discover(self) -> Union[TreeData, None]:
        """Load environment variables.

        These are loaded only for performing the initial override settings step. They
        are not used for run-time resolution of keys.

        .. note::

            This loads all environment variables, both with and without the defined
            standard prefix.

        :return: A :class:`TreeData` with the prefix stripped from all names
        """
        data = {key: item for key, item in os.environ.items()}

        # Replicate keys to name with the prefix stripped off
        updates = {self.get_root_var_name(key): item for key, item in data.items()}
        data.update(updates)

        return TreeData(**data)

    @to_variable
    def resolve(self, variable: Union[Variable, str], safe: bool = False) -> Union[Resolution, None]:
        """Resolve from :class:`os.environ`.

        This will look for the name with/without the standard variable prefix.

        This inspects the "live" environ variable by name.

        :param variable: Alternate resolve source
        :param safe: True to return None if not resolved (else raise:class:`NotResolvedError`)
        :return: The resolved value
        :raises NotResolvedError: If not found in the ``os.environ``

        """
        alt_name: str = self.toggle_name_prefix(name=variable.var_name)

        matches = [os.environ.get(n) for n in {alt_name, variable.var_name}]
        match = next((m for m in matches if m), None)
        if not match:
            raise NotResolvedError(name=variable.var_name)

        return Resolution(value=variable.apply_type_hint(value=match))
