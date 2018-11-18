from views import index


api_urls = []

other_urls = [
    ("/", index, ["GET"], "index url"),
]

all_urls = api_urls + other_urls
