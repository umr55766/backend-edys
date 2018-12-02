def get_paginated_list(model, url, start, limit, serializer):
    count = model.query.count()
    if start > count != 0:
        return {"error": "invalid page"}

    return {
        'start': start,
        'limit': limit,
        'count': count,
        'previous': get_previous_url(start, limit, url),
        'next': get_next_url(start, limit, count, url),
        'results': get_serialized_data(model, start, limit, serializer)
    }


def get_next_url(start, limit, count, url):
    if start + limit > count:
        return None
    else:
        start_copy = start + limit
        return url + '?start=%d&limit=%d' % (start_copy, limit)


def get_previous_url(start, limit, url):
    if start == 1:
        return None
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        return url + '?start=%d&limit=%d' % (start_copy, limit_copy)


def get_serialized_data(object, start, limit, serializer_class):
    objects = object.query.all()
    objects = objects[(start - 1):(start - 1 + limit)]
    serializer = serializer_class.dump(objects)
    return serializer.data
