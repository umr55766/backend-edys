from app import rq


@rq.job
def add(x, y):
    return x + y
