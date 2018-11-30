from flask import Flask, jsonify
from flask import request

from decouple import config
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy
from rq import Connection, Queue
from sqlalchemy_utils import URLType
import redis
import requests

from src.utils import get_paginated_list

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
        page_word_count = PageWordCount(url=url, word_count=len(response.text.split()))
        db.session.add(page_word_count)
        db.session.commit()
        print("Saved successfully")


@application.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return jsonify(
            get_paginated_list(
                model=PageWordCount,
                url=request.base_url,
                start=int(request.args.get('start', 1)),
                limit=int(request.args.get('limit', 20)),
                serializer=page_word_counts_serializer,
            )
        )

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


@application.route("/tasks/<task_id>", methods=['GET',])
def task_details_view(task_id):
    with Connection(redis.from_url(config('REDIS_URL'))):
        queue = Queue()
        task = queue.fetch_job(task_id)

    if task:
        response = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_status': task.get_status(),
                'task_result': task.result,
            }
        }
    else:
        response = {'status': 'error'}

    return jsonify(response)
