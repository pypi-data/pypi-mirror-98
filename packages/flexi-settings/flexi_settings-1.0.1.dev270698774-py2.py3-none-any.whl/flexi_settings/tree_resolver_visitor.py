"""Resolver for tree data."""

from typing import List, Any

from jmespath.exceptions import LexerError

from flexi_settings.resolver import NotResolvedError, Resolution, Resolver
from flexi_settings.tree_data import UNDEFINED_MAGIC
from flexi_settings.variable import VariableString, Variable
from flexi_settings.visitors import TreeDataVisitor


class TreeResolverVisitor(TreeDataVisitor):
    """For fully resolving all variables found within a dict/TreeData node.

    This traverses a node (generally a dict), finding and resolving any embedded
    variables from the passed-in list of :class:`Resolver` items.

    """

    def __init__(self, resolvers: List[Resolver]):
        """Construct.

        If the data passed into :meth:`visit` may also be used to resolve
        variables, it should be wrapped in a
        :class:`TreeDataResolver <tree_data_resolver.TreeDataResolver>`
        and be included in the list of resolvers. (This will generally be the case.)

        :param resolvers: List of :class:`Resolver <resolver.Resolver>` items ordered by priority
        """
        super().__init__()

        self.resolvers: List[Resolver] = resolvers

    def visit_dict_item(self, key, value) -> Any:
        """Visit dict item.

        :meta private:
        :param key:
        :param value:
        :return:
        """
        if isinstance(value, str):
            return self.visit_scalar(value)

        return super().visit_dict_item(key=key, value=value)

    def visit_scalar(self, node) -> Any:
        """Visit a scalar node.

        :meta private:
        :param node: The scalar node
        :raises NotResolvedError: If the/an embedded variable can not be resolved
        """
        # We're only concerned with strings. Return anything else untouched.
        if not isinstance(node, str):
            return node

        var_string = VariableString(string=node)

        # Are there variables found within the node/string?
        if not var_string.has_vars:
            return node

        return self.resolve_scalar(var_string=var_string)

    def get_field(self, string: str, recursive: bool = False, default: Any = UNDEFINED_MAGIC) -> Any:
        """Get a single field by either name or variable template.

        This should be used *only* for getting a single field. The parameter
        ``string`` may be either the field signature, or be wrapped as a
        field variable template.

        This will recursively resolve the value(s) if the ``recursive`` parameter is True.

        :param string: A simple field name or variable template
        :param recursive: True to recursively resolve the field if it also contains a variable(s)
        :param default: Optional default if the field is not resolved
        :raises NotResolvedError: If not resolved and ``default`` is not supplied
        """
        var_str = VariableString(string=string)
        if var_str.has_vars and len(var_str) > 1:
            raise ValueError('Only a single variable can be resolved with "get_field". {}'.format(
                string
            ))

        try:
            # TODO: If string is just a field name this will bomb - there are no "vars"

            # First try direct lookup of the variable
            resolved = self.resolve_variable(variable=var_str.first, default=default)
            if recursive and resolved.has_vars():
                return self.visit(node=resolved.value)

            return resolved.value

        except NotResolvedError:
            if default != UNDEFINED_MAGIC:
                return default
            raise

    def resolve_scalar(self, var_string: VariableString) -> Any:
        """Resolve the string with embedded variable.

        :meta private:
        :param var_string: A VarString value to resolve
        :raises NotResolvedError: If the/an embedded variable can not be resolved
        """
        if var_string.is_single_var():
            return self.resolve_simple(variable=var_string.first)

        # Resolve a string with non-var characters or multiple variables
        return self.resolve_string(string=var_string.string)

    def resolve_string(self, string: str) -> Any:
        """Resolve a string containing embedded variable(s).

        .. warning::

            This does not recursively resolve variables and can potentially return
            a string with embedded variables.

        .. note::

            Simple strings with a single variable are resolved via :meth:`resolve_simple`.

        *Examples*

        .. code-block: python

            "Embedded !VAR! string"  # ==> "Embedded variable string"
            "!DB_HOST:str!:!DB_PORT!"  # ==> "rdbtest.eng.msx.rocks:28015"

        :param string: The string to resolve vars within
        :raises NotResolvedError: If the/an embedded variable can not be resolved
        """

        def repl_func(match):
            """Called by the regex ``.sub()`` method on matches"""
            variable = Variable.from_re_match(match=match)
            variable.var_type = 'str'  # the ".sub" call requires a string return

            resolution = self.resolve_variable(variable=variable)
            return resolution.value

        return VariableString.re_embedded_var.sub(repl_func, string)

    def resolve_simple(self, variable: Variable) -> Resolution:
        """Resolve a simple, single variable.

        This will recursively resolve the variable if it also contains variable
        templates.

        :param variable: A :class:`Variable <variable.Variable>` item
        :raises NotResolvedError: If the/an embedded variable can not be resolved
        """
        assert isinstance(variable, Variable)

        resolved = self.resolve_variable(variable=variable)
        if not resolved.has_vars():
            return resolved

        # Is this a complex resolution?
        if self.is_array_like(resolved.value):
            return self.visit(resolved.value)

        embedded = VariableString(string=resolved.value)
        if embedded.is_single_var():
            return self.resolve_simple(variable=embedded.first)

        # The resolution is a string with one or more variables
        while True:
            resolved = self.resolve_string(string=resolved.value)
            if not resolved.has_vars:
                return resolved

    def resolve_variable(self, variable: Variable, default: Any = UNDEFINED_MAGIC) -> Resolution:
        """Resolve a single variable with our list of resolvers.

        This will apply type hinting if specified. If the parameter default is supplied, or if
        the ``variable`` contains a default, if the variable can not be resolved one of
        the defaults are returned.

        The precedence for defaults is:

        1. The parameter to this method
        2. The default in ``variable``

        :param variable: A :class:`Variable <variable.Variable>` item
        :param default: Optional default
        :raises NotResolvedError: If the variable can not be resolved and ``default`` is not supplied
        """
        for resolver in self.resolvers:
            try:
                value = resolver.resolve(variable=variable)
                return value

            except LexerError:
                raise  # Just here for a debugger breakpoint
            except NotResolvedError:
                pass
            except Exception as ex:
                print(ex)
                raise

        # If no parameter default supplied, apply the default from the variable
        default = variable.default if default == UNDEFINED_MAGIC else default

        if default == UNDEFINED_MAGIC:
            raise NotResolvedError(name=variable.var_name)

        # Return the default with type hinting applied
        return Resolution(value=variable.apply_type_hint(default))
