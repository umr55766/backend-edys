from flask import Flask, jsonify

from decouple import config


def create_app(TEST=False):
    application = Flask(config("APPLICATION_NAME"))
    if TEST:
        application.config.from_pyfile("settings/test.py")
    else:
        application.config.from_pyfile(config("SETTINGS_FILE", "settings/local.py", cast=str))

    from .models import db, migrate
    db.init_app(application)
    migrate.init_app(application, db)

    from .serializers import ma
    ma.init_app(application)

    from .tasks import rq
    rq.init_app(application)

    from .views import api_views
    application.register_blueprint(api_views)

    from .commands import CLI_COMMANDS
    for cli_name, cli_command in CLI_COMMANDS.items():
        application.cli.add_command(cli_command, name=cli_name)

    return application
