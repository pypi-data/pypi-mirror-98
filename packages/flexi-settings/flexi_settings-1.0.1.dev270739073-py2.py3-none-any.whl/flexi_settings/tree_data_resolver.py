"""Resolver from dict-like TreeData."""
import os
from typing import Union

from flexi_settings import to_variable
from flexi_settings.resolver import NotResolvedError, Resolution, Resolver
from flexi_settings.tree_data import JmesNotFound, NoneValueVisitor, TreeData

# TODO: Add a "watcher" that can be enabled to dynamically reload file data on change
from flexi_settings.variable import Variable


class TreeDataResolver(Resolver):
    """To resolve variables from :class:`TreeData <tree_data.TreeData>` content.

    This uses jmespath to locate the variable in the dictionary. Note that the
    value returned by :meth:`resolve` could be/contain other variable(s).

    **Example Usage:**

    .. code-block:: yaml

        DB_HOST: cloud
        RABBITMQ_HOST: cloud
        OPTIONS:
          one: 1
          two: 2

    Given the above YAML file:

    .. code-block:: python

        resolver = TreeDataResolver(tree_data=data)

        resolver.get_field("!DB_HOST!")  # "cloud"
        resolver.get_field("!OPTIONS.one!")  # 1
        resolver.get_field("!UNKNOWN!", default=None)  # None
        resolver.get_field("!UNKNOWN!")  # Raises NotResolvedError()

    """

    def __init__(self, filename: str = None,
                 tree_data: TreeData = None,
                 data: dict = None,
                 name: str = 'tree_resolver'):
        """Construct from either filename, TreeData or dict data.

        Any of the three parameters may be used to create an instance. The precedence
        (if multiple parameters are supplied - which should not be the case...) is:

        1. filename
        2. tree_data
        3. data
        4. raise :class:`ValueError` if all 3 are None

        :param filename: The filename to a JSON/YAML file
        :param data: Optional dict with the data
        :param tree_data: Optional :class:`TreeData`
        :param name:
        :raises ValueError: Missing a data reference
        :raises FileNotFoundError: If ``filename`` is not found
        """
        self.filename: str = filename
        super().__init__(name)

        if not any([filename, tree_data, data]):
            raise ValueError('Must supply either filename, tree_data or data')

        self.content = self.discover() or tree_data or TreeData(**data)

    def discover(self) -> Union[TreeData, None]:
        """For loading from a file if `filename` is passed to our constructor."""
        if not self.filename:
            return None

        if not os.path.exists(self.filename):
            raise FileNotFoundError('Yaml file does not exist: {}'.format(self.filename))

        return TreeData.load(self.filename)

    @to_variable
    def resolve(self, variable: Union[Variable, str], safe: bool = False) -> Union[Resolution, None]:
        """Resolve from the the :class:`TreeData <tree_data.TreeData>` content.

        .. note::

            * Returns deepcopy of the resolution.
            * Replaces NONE_MARKER(s) if present with None in returned data

        :param variable: Alternate resolve source
        :param safe: True to return None if not resolved rather than raise :class:`NotResolvedError`
        :return: A Resolution, or None (if safe==True) if not resolved
        """
        from copy import deepcopy

        try:
            result = self.content.jmesquery(query=variable.var_name)

            reply = Resolution(value=variable.apply_type_hint(deepcopy(result)))

            # Restore any NONE_MARKER placeholders back to None if present
            NoneValueVisitor(restore_none=True).visit(reply.value)

            return reply

        except JmesNotFound:
            if not safe:
                raise NotResolvedError(message=variable.var_name)
            return None
