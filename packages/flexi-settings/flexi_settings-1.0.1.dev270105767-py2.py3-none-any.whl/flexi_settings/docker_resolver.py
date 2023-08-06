"""Resolver for Docker swarm secrets/configs.

Loads and Resolves variables from files mounted by Docker containing variables
for swarm secrets and configs.

"""
import os
from typing import Union, Dict, Any

from flexi_settings import to_variable
from flexi_settings.resolver import NotResolvedError, Resolution, Resolver
from flexi_settings.variable import Variable


class DockerSwarmResolver(Resolver):
    """Base class for Docker swarm resolvers.

    Both Docker swarm configs and secrets are supplied to a service instance by mounting
    the value in a file within the container. (Note: We do not as yet use these.)

    This will discover existing items on construction. Then, the :meth:`resolve` will
    continue to look for the value in the file on-demand to pick up the current value.

    .. note::

        Docker allows both configs and secrets to be updated for a service while it
        is running. As such, we still open the file to fetch the current value on-demand.

    .. note::

        By definition (I think it might be a Docker thing, but if not, we should
        standardize on using all upper case variables. "VARIABLE" rather than "variable".

    """

    default_configs_dir = "/"
    """The default mount directory for Docker swarm configs (SWARM_CONFIG_DIR)"""
    default_secrets_dir = "/run/secrets"
    """The default mount directory for Docker swarm secrets (SWARM_SECRET_DIR)"""

    def __init__(self, name: str = 'docker_resolver', root_dir: str = "/"):
        """Construct.

        :param name:
        :param root_dir: The directory the Swarm configs/secrets are mounted to
        """
        super().__init__(name)
        self.root_dir = os.path.realpath(root_dir)

        # self.variables: dict = {}
        """The discovered variables on creating this"""

        self.discover()

    def discover(self, only_upper: bool = True):
        """Discover the items that are found in the :attr:`root_dir`.

        If ``only_upper`` is True, this searches for files with upper-case names only.
        It loads all files found, but converts names with the standard prefix stripped off.
        Internally both with, and without the prefix are stored.

        :param only_upper: True if the filename is only upper-case
        """
        with os.scandir(self.root_dir) as files:  # noqa: W503
            contents = [item.name for item in files if item.is_file() and  # noqa: W504
                        (not only_upper or item.name.isupper())]

        variables: Dict[str, Any] = {}

        for name in contents:
            root_name = self.get_root_var_name(name_with_prefix=name)
            resolution = self.resolve(variable=name)
            variables[root_name] = resolution.value

        self.set_content(dict_vars=variables)

    @to_variable
    def resolve(self, variable: Union[Variable, str], safe: bool = False) -> Union[Resolution, None]:
        """Resolve from Docker swarm configs/secrets files.

        This does not cache the result. Per the Docker docs:  "You can update a service
        to grant it access to additional secrets or revoke its access to a given secret at
        any time."

        Note: This will look for the variable both with and without the standard prefix. If
        the variable exists in both forms, there is no guarantee which is returned.

        .. note::

            This is case-sensitive if the underlying filesystem supports.

        :param variable: Variable to resolve
        :param safe: True to return None if not resolved rather than raise :class:`NotResolvedError`
        :return: A Resolution, or None (if safe==True) if not resolved
        """
        names = [variable.var_name, self.toggle_name_prefix(variable.var_name)]

        for _name in names:
            filename = os.path.join(self.root_dir, _name)

            if not os.path.exists(filename):
                continue

            with open(filename) as fp:
                value = fp.read()
                resolution = Resolution(value=variable.apply_type_hint(value.strip()))
                return resolution

        if not safe:
            raise NotResolvedError(message=variable.var_name)

        return None


class DockerConfigsResolver(DockerSwarmResolver):
    """Wrapper for Docker config file keys."""

    def __init__(self, name: str = 'docker_configs', root_dir: str = DockerSwarmResolver.default_configs_dir):
        super().__init__(name, root_dir)


class DockerSecretsResolver(DockerSwarmResolver):
    """Wrapper for Docker secrets file keys."""

    def __init__(self, name: str = 'docker_secrets', root_dir: str = DockerSwarmResolver.default_secrets_dir):
        super().__init__(name, root_dir)

    def discover(self, only_upper: bool = True):  # noqa: D102
        return super().discover(only_upper=False)
