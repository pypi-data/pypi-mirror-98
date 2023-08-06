"""Example simple Flask API service.

This service demonstrates a simple API server that connects
to a RethinkDB and provides a set of routes for API calls.

Flask may be configured from upper-case variables. For this we
will use Flask's ``app.config.from_object(config)`` method, and
in our settings will prefix variables to expose with the prefix
"FLASK\_".

"""

from flexi_settings import module_dir
# from flask import Blueprint, Flask

from flexi_settings.base_settings import ServiceSettings
from flexi_settings.context import SettingsContext, SettingsContextSingleton
import examples.flask_api_service.fake_db as fake_db


def setup_context() -> SettingsContext:
    context = SettingsContext(
        service_name='api_service',
        var_prefix="XYZ_",
        settings_root_dir=module_dir(name_or_module=fake_db.__name__),
        settings_filename='settings.yml'
    )

    return SettingsContextSingleton.instance(context=context)


def main():
    context = setup_context()
    settings = ServiceSettings(settings_context=context)

    # TODO: Finish example


if __name__ == '__main__':
    main()
