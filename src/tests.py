import json
import unittest
from time import sleep

from flask import Flask, current_app

from flask_testing import TestCase


class BaseTestCase(TestCase):
    def create_app(self):
        from app import create_app
        return create_app(True)

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
