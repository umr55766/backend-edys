from flask_rq2 import RQ
import requests

from .models import db, PageWordCount


rq = RQ()


@rq.job
def count_words_task(url):
    response = requests.get(url)
    if response.status_code == 200:
        page_word_count = PageWordCount(url=url, word_count=len(response.text.split()))
        db.session.add(page_word_count)
        db.session.commit()
        print("Saved successfully")
