from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import URLType


db = SQLAlchemy()
migrate = Migrate()


class PageWordCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(URLType)
    word_count = db.Column(db.Integer)
