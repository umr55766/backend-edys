import json
import unittest
from time import sleep

from flask import Flask, current_app

from flask_testing import TestCase
from decouple import config


class BaseTestCase(TestCase):
    def create_app(self):
        application = Flask(config("APPLICATION_NAME"))
        application.config.from_pyfile("settings/test.py")

        from models import db, migrate
        db.init_app(application)
        migrate.init_app(application, db)

        from serializers import ma
        ma.init_app(application)

        from tasks import rq
        rq.init_app(application)

        from views import api_views, html_views
        application.register_blueprint(api_views)
        application.register_blueprint(html_views)

        from commands import CLI_COMMANDS
        for cli_name, cli_command in CLI_COMMANDS.items():
            application.cli.add_command(cli_command, name=cli_name)

        return application

    def setUp(self):
        from models import db
        db.create_all()

    def tearDown(self):
        from models import db
        db.session.remove()
        db.drop_all()


class APITest(BaseTestCase):
    def test_empty_database(self):
        response = self.client.get("/api/list")
        assert response.status_code == 200
        assert response.json["count"] == 0

    def test_posting_url(self):
        response = self.client.post("/api/list", data=json.dumps({"url": "https://umair.surge.sh"}))
        assert response.status_code == 200
        assert "task_id" in response.json

    def test_task_status_checking(self):
        response = self.client.post("/api/list", data=json.dumps({"url": "https://umair.surge.sh"}))
        task_id = response.json["task_id"]

        response = self.client.get("api/tasks/%s" % task_id)
        assert response.json["status"] == "success"

    def test_integrated(self):
        response = self.client.post("/api/list", data=json.dumps({"url": "https://umair.surge.sh"}))
        task_id = response.json["task_id"]

        response = self.client.get("api/tasks/%s" % task_id)
        while response.json["data"]["task_status"] not in ["finished", "failed"]:
            sleep(1)
            response = self.client.get("api/tasks/%s" % task_id)

        response = self.client.get("/api/list")
        assert response.json["count"] == 1
        assert response.json["count"] == 1


if __name__ == '__main__':
    unittest.main()
