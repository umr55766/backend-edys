from flask import Flask

from decouple import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

application = Flask(config("APPLICATION_NAME"))
SETTINGS_FILE = config("SETTINGS_FILE", "settings/local.py")
application.config.from_pyfile(SETTINGS_FILE)

db = SQLAlchemy(application)
migrate = Migrate(application, db)
