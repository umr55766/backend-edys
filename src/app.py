import requests

from flask import Flask
from flask import request

from decouple import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_rq2 import RQ
from sqlalchemy_utils import URLType

application = Flask(config("APPLICATION_NAME"))
SETTINGS_FILE = config("SETTINGS_FILE", "settings/local.py", cast=str)

application.config.from_pyfile(SETTINGS_FILE)

db = SQLAlchemy(application)
migrate = Migrate(application, db)
rq = RQ(application)


@rq.job
def count_words_task(url):
    response = requests.get(url)
    if response.status_code == 200:
        page_word_count = PageWordCount(url=url, word_count=len(str(response.content).split(" ")))
        db.session.add(page_word_count)
        db.session.commit()
        print("Saved successfully")


@application.route("/")
def index():
    url = request.args.get('url')
    count_words_task.queue(url)
    return count_words_task.queue(url).id


class PageWordCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(URLType)
    word_count = db.Column(db.Integer)
