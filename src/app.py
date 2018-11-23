import os

from flask import Flask

from decouple import config

application = Flask(config("APPLICATION_NAME"))
