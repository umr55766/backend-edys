from flask import Blueprint, request, jsonify, render_template

from decouple import config
from rq import Connection, Queue
import redis

from .models import PageWordCount
from .serializers import page_word_counts_serializer
from .tasks import count_words_task
from .utils import get_paginated_list, get_serialized_data

api_views = Blueprint('api', __name__, url_prefix='/api')
html_views = Blueprint('html', __name__)


@api_views.route("/datatable", methods=['GET', ])
def datatable_data():
    return jsonify(
        {
            "data": [[obj["id"], obj["url"], obj["word_count"]] for obj in get_serialized_data(
                object=PageWordCount,
                start=1,
                limit=int(request.args.get("limit", 1000)),
                serializer_class=page_word_counts_serializer)]
        })


@api_views.route("/list", methods=['GET', 'POST'])
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

    if not request.get_json(force=True) or "url" not in request.get_json(force=True):
        return jsonify({"url": "is required"})

    url = request.get_json().get('url')
    task = count_words_task.queue(url)
    return jsonify({"task_id": task.id})


@api_views.route("/tasks/<task_id>", methods=['GET', ])
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


@html_views.route("/", methods=["GET", ])
def index_view():
    return render_template('index.html', page_word_counts = PageWordCount.query.all())
