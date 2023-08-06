"""Example of creating a domain-specific, custom settings class."""

from dataclasses import dataclass

from flexi_settings.base_settings import ServiceSettings


@dataclass
class DBInfo(object):
    host: str
    user: str
    pwd: str
    port: int = 4567


class CustomSettings(ServiceSettings):
    """Domain-specific settings class.

    This demonstrates how to create a wrapper to make access to some
    common fields easier. For example, in our context with our main
    API service we very often need to access the settings DB info fields
    to make requests against the database.  By creating a wrapper like
    this we remove the need to know the actual settings key names.

    """

    @property
    def db_host(self) -> str:
        """Get the DB_HOST field.

        The field name may be stated without delimiters.

        """
        return self.get_field('DB_HOST')

    @property
    def db_port(self) -> int:
        """Get the DB_PORT field as int.

        In this case the field is stated with delimiters - but does not
        need to be.

        """
        return self.get_field('!DB_PORT:int!')

    @property
    def db_settings(self) -> DBInfo:
        """Get the settings as a dataclass."""
        info = DBInfo(
            host=self.get_field('DB_HOST'),
            user=self.get_field('DB_USER'),
            pwd=self.get_field('DB_PWD'),
            port=self.get_field('DB_PORT')
        )
        return info

    @property
    def custom_message(self) -> str:
        """Get example of generating a string with embedded fields."""
        msg = "The DB Info is: Host=!DB_HOST! Port=!DB_PORT! User=!DB_USER! Pwd=!DB_PWD!"
        return self.update_string(str_with_fields=msg)

    @classmethod
    def hack_field_value(cls, new_host):
        """Update a field value with environment variable.

        While silly, this is a legit method for dynamically updating a field's value
        with an environment variable. By setting the env_var, the
        :class:`EnvVarResolver <env_resolver.EnvVarResolver>` will pick
        up the override.

        Generally, for a Docker swarm service the hostname would be updated by
        updating an environment variable via Docker, or via Docker configs.

        """
        import os

        os.environ['DB_HOST'] = new_host
