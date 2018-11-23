from flask import Flask

from decouple import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_rq2 import RQ

application = Flask(config("APPLICATION_NAME"))
SETTINGS_FILE = config("SETTINGS_FILE", "settings/local.py")

# TODO : Needs to be investigated and fixed
# rqworker : __file__ = ./src/app.py
# flask run : __file__ = /Users/umair/workspace/edyst/backend-edys/src/app.py
SETTINGS_FILE = ("src/" if __file__[0] == "." else "") + SETTINGS_FILE

application.config.from_pyfile(SETTINGS_FILE)

db = SQLAlchemy(application)
migrate = Migrate(application, db)
rq = RQ(application)


@rq.job
def add(x, y):
    return x + y

@application.route("/")
def index():
    add.queue(1, 1)
    # from .tasks import add
    return "Welcome!"
