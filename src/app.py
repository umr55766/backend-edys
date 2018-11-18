from __future__ import absolute_import, unicode_literals

from flask import Flask

from decouple import config

from urls import all_urls


application = Flask(config("APPLICATION_NAME"))
SETTINGS_FILE = config("SETTINGS_FILE", default="settings.local1")

application.config.from_object(SETTINGS_FILE)


# Adding all the url rules in the application
for url, view, methods, _ in all_urls:
    application.add_url_rule(url, view_func=view, methods=methods)
