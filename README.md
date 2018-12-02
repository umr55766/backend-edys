# Exposed APIs:

- API to list of all submitted urls : GET request to index url `/`
  - Example : curl --request GET --url 'http://127.0.0.1:5000/?limit=5'  --header 'Content-Type: application/javascript'
- API to submit a url : POST request to index url `/`
  - Example : curl --request POST --url http://127.0.0.1:5000/ --header 'Content-Type: application/javascript' --data '{\n    "url": "https://umair.surge.sh"\n}'
- API to check status of background task : GET request to `/tasks/<task_id>`
  - Example : curl --request GET --url http://127.0.0.1:5000/tasks/5f19ef59-81a2-46af-a104-2ccc6d087029

### Workflow:

- Make a POST request to `/` index url with your url in body with the key `url`
- You'll get the background task_id in response
- You can check the background task status by making GET request to `/tasks/<task_id>`
- To get the results you can make GET request to `/` index url
   -  **_This API supports pagination. Client can control page size by sending page size in query params with `limit` as key_**


#### Steps to run this project:

- (Recommended) Install and create virtualenv and activate the same
- Clone this repository to your local [`git clone https://github.com/umr55766/backend-edys.git`]
- Go into root directory [`cd backend-edys/`]
- Install the requirements [`pip install -r requirements.txt`]
- Set `FLASK_APP` environment variable to `app.py` [For Linux: `export FLASK_APP=app.py`]
- Go into source directory [`cd src/`]
- Run `flask run`


#### Steps to run background task worker:

- Set `FLASK_APP` environment variable to `app.py` [For Linux: `export FLASK_APP=app.py`]
- First we need to start the redis [`redis-server`]
- Then start rqworker which will consume the queued tasks and process them [`flask rq worker`]


**Libraries used and purpose**
- flask-sqlalchemy : ORM
- python-decouple : Refactor settings out to hidden file
- Flask-Migrate : Manage model migrations
- Flask-RQ2 : Background tasks
- redis : Background task backend/storage
- requests : HTTP Client
- flask-marshmallow : Serializer

**Sample API response**
```{
  "start": 6,
  "limit": 5,
  "count": 16,
  "previous": "http://127.0.0.1:5000/?start=1&limit=5",
  "next": "http://127.0.0.1:5000/?start=11&limit=5",
  "results": [
    {
      "id": 6,
      "url": "https://umair.surge.sh",
      "word_count": 12768
    },
    {
      "id": 7,
      "url": "http://umair.surge.sh",
      "word_count": 12768
    },
    {
      "id": 8,
      "url": "http://umair.surge.sh",
      "word_count": 12768
    },
    {
      "id": 9,
      "url": "http://umair.surge.sh",
      "word_count": 12768
    },
    {
      "id": 10,
      "url": "http://umair.surge.sh",
      "word_count": 1363
    }
  ]
}
