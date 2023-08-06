"""Visitor to apply static overrides."""
from typing import List

from flexi_settings.tree_data import TreeData, NONE_MARKER, JmesNotFound
from flexi_settings.visitors import TreeDataVisitor


class OverrideVisitor(TreeDataVisitor):
    """For overwriting keys in a target from an override source.

    This is to update the primary settings with overrides to produce a consolidated
    :class:`TreeData <tree_data.TreeData>`.

    The supplied ``overrides`` list should be in priority order from highest-to-lower. Internally
    we will reverse the order for iterating such that the highest priority will override the
    others.

    **Usage Example**

    Load a primary settings YAML file and apply overrides from both environ variables and
    Docker swarm secrets.

    .. code-block:: python

        env_data = EnvVarResolver()
        docker_data = DockerSecretsResolver()
        settings = TreeData.load('settings.yml')

        consolidated = OverrideVisitor([env_data.contents, docker_data.contents]).visit(settings)

    """

    def __init__(self, overrides: List[TreeData]):
        """Construct.

        :param overrides: List of :class:`TreeData` items in priority order highest-to-lower
        """
        super().__init__()

        # The list of overrides in reversed order
        self.overrides = list(reversed(overrides))

    def visit_dict_item(self, key, value):
        """Look for this key in overrides.

        This uses the "stack" as the jmespath query term.

        :meta private:
        """
        _value = NONE_MARKER

        for override in self.overrides:
            try:
                _value = override.jmesquery(query=self.key_stack_string)

            except JmesNotFound:
                pass
            except AttributeError:
                pass

        return _value if _value != NONE_MARKER else value
