from __future__ import absolute_import, unicode_literals
import os

from flask import Flask

from urls import all_urls


application = Flask(os.environ.get("APPLICATION_NAME"))
SETTINGS_FILE = os.environ.get("SETTINGS_FILE", "settings.local")

application.config.from_object(SETTINGS_FILE)


# Adding all the url rules in the application
for url, view, methods, _ in all_urls:
    application.add_url_rule(url, view_func=view, methods=methods)
