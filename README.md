# Exposed APIs:

- API to list of all submitted urls : GET request to index url `/`
- API to submit a url : POST request to index url `/`
- API to check status of background task : GET request to `/tasks/<task_id>`

### Workflow:

- Make a POST request to `/` index url with your url in body with the key `url`
- You'll get the background task_id in response
- You can check the background task status by making GET request to `/tasks/<task_id>`
- To get the results you can make GET request to `/` index url


#### Steps to run this project:

- (Recommended) Install and create virtualenv and activate the same
- Clone this repository to your local [`git clone https://github.com/umr55766/backend-edys.git`]
- Go into root directory [`cd backend-edys/`]
- Install the requirements [`pip install -r requirements.txt`]
- Set `FLASK_APP` environment variable to `app.py` [For Linux: `export FLASK_APP=app.py`]
- Go into source directory [`cd src/`]
- Run `flask run`


#### Steps to run background task worker:

- First we need to start the redis [`redis-server`]
- Then start rqworker which will consume the queued tasks and process them [`flask rq worker`]
