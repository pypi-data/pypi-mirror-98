"""Variable resolver from contained list of :class:`Resolver <resolver.Resolver>` items."""
from typing import List

from flexi_settings.resolver import Resolver
from flexi_settings.tree_resolver_visitor import TreeResolverVisitor
from flexi_settings.variable import VariableString
from flexi_settings.visitors import HasVariablesVisitor


class VariableResolver(TreeResolverVisitor):
    """Wrapper for :class:`TreeResolverVisitor <tree_resolver_visitor.TreeResolverVisitor>`

    This helper class is the primary revolver that
    :class:`ServiceSettings <base_settings.ServiceSettings>` uses for getting field key
    values and resolving variables.

    """

    def __init__(self, resolvers: List[Resolver]):
        super().__init__(resolvers)

    @classmethod
    def has_variable(cls, node: str) -> bool:
        """Test if ``node`` contains any embedded vars.

        This uses :class:`HasVariablesVisitor <visitors.HasVariablesVisitor>` to search
        for any variable templates within it. If ``node`` is a simple string this
        just searches for
        :const:`TreeResolverVisitor.re_embedded_var <tree_resolver_visitor.TreeResolverVisitor.re_embedded_var>`
        within the string.

        """  # noqa: W505
        if isinstance(node, str):
            return VariableString.str_has_vars(string=node)

        return HasVariablesVisitor().check(node=node)

    def add_resolver(self, resolver: Resolver, priority: bool = False) -> None:
        """Add a custom resolver.

        To add a resolver at the top of the list such that it the first to be used
        to resolve a variable name.

        :param resolver: A Resolver instance
        :param priority: If True, this resolver is pushed to the top of the list
        :return:
        :raises ValueError: If resolver is not of class Resolver
        """
        if not isinstance(resolver, Resolver):
            raise ValueError('Resolvers must be of class type Resolver for add_resolver')

        if priority:
            self.resolvers.insert(0, resolver)
        else:
            self.resolvers.append(resolver)
