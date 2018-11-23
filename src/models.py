from sqlalchemy_utils import URLType

from app import db


class PageWordCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(URLType)
    word_count = db.Column(db.Integer)
