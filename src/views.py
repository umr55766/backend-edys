from app import application


@application.route("index/")
def index():
    return "Welcome!"
