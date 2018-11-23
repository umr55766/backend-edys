from flask import Flask

from decouple import config

application = Flask(config("APPLICATION_NAME"))
SETTINGS_FILE = config("SETTINGS_FILE", "settings.local.py")
application.config.from_pyfile(SETTINGS_FILE)
