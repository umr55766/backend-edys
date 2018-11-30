import requests

from flask import Flask, jsonify
from flask import request

from decouple import config
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import URLType


application = Flask(config("APPLICATION_NAME"))
SETTINGS_FILE = config("SETTINGS_FILE", "settings/local.py", cast=str)

application.config.from_pyfile(SETTINGS_FILE)

db = SQLAlchemy(application)
migrate = Migrate(application, db)
rq = RQ(application)
ma = Marshmallow(application)


@rq.job
def count_words_task(url):
    response = requests.get(url)
    if response.status_code == 200:
        page_word_count = PageWordCount(url=url, word_count=len(str(response.content).split(" ")))
        db.session.add(page_word_count)
        db.session.commit()
        print("Saved successfully")


@application.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        page_word_counts = PageWordCount.query.all()
        serializer = page_word_counts_serializer.dump(page_word_counts)
        return jsonify(serializer.data)

    url = request.args.get('url')
    task = count_words_task.queue(url)
    return jsonify({"task_id": task.id})


class PageWordCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(URLType)
    word_count = db.Column(db.Integer)


class PageWordCountSerializer(ma.Schema):
    class Meta:
        fields = ('id', 'url', 'word_count')


page_word_count_serializer = PageWordCountSerializer()
page_word_counts_serializer = PageWordCountSerializer(many=True)
