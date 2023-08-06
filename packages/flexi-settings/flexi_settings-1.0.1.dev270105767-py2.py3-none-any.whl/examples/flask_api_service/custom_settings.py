"""A custom :class:`ServiceSettings <base_settings.ServiceSettings>` class."""

from flexi_settings.base_settings import ServiceSettings


class FlaskSettings(object):
    """A class that will contain all the variables in settings for Flask.

    All of the upper-case keys with a prefix of "FLASK\_" will be set to self.

    """

    def __init__(self, settings: ServiceSettings):
        self.filter_flask_settings(settings=settings)

    def filter_flask_settings(self, settings: ServiceSettings):
        """Find all FLASK\\_ settings and set to self."""
        keys = [str(key) for key in settings.settings.keys() if str(key).startswith('FLASK_')]

        for name in keys:
            # Fetch the value from the settings
            value: str = settings.get_field(name)

            # Strip off the prefix
            value = value.replace('FLASK_', '').upper()  # Will prolly already be upper-case

            # Set the key/value to self as attribute
            setattr(self, name, value)

