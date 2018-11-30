from collections import OrderedDict

from flask import Flask, jsonify
from flask import request

from decouple import config
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import URLType
import requests


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
                limit=int(request.args.get('limit', 20)))
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


def get_paginated_list(model, url, start, limit):
    count = model.query.count()
    if count < start:
        return {"error": "invalid page"}

    return {
        'start': start,
        'limit': limit,
        'count': count,
        'previous': get_previous_url(start, limit, url),
        'next': get_next_url(start, limit, count, url),
        'results': get_serialized_data(model, start, limit, page_word_counts_serializer)
    }


def get_next_url(start, limit, count, url):
    if start + limit > count:
        return None
    else:
        start_copy = start + limit
        return url + '?start=%d&limit=%d' % (start_copy, limit)


def get_previous_url(start, limit, url):
    if start == 1:
        return None
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        return url + '?start=%d&limit=%d' % (start_copy, limit_copy)


def get_serialized_data(object, start, limit, serializer_class):
    objects = object.query.all()
    objects = objects[(start - 1):(start - 1 + limit)]
    serializer = serializer_class.dump(objects)
    return serializer.data
