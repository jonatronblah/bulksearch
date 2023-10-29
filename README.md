# bulksearch
application for executing bulk async elasticsearch queries via spreadsheet - posted here for educational purposes.

## project structure
application components are in named directories: api, client. docker configuration and deployment is defined in deploy directory.

## application structure
all app components are run via docker containers. see deploy/docker-compose.yml

### elasticsearch
cluster of containers to run local elasticsearch instance. see deploy/es.docker-compose.yml

### api
python backend using FastAPI web framework. provides user authentication, db model definitions, data parsing and manipulation logic, connection to elasticsearch for users

### client
web interface for application using reactjs via vite. sends/receives user data and authentication headers/cookies to/from the backend. also parses user uploaded documents to provide data to the backend.

### db
postgres database instance to store backend data (only user authentication data at this point)

### migrator
based off api container image - checks for and upgrades database changes on app start via alembic migration scripts. alembic is a popular python package for managing database migrations.

### worker
python container based off api container image - runs a worker for background tasks via celery, a python library for scheduling and running background tasks.

### celery-beat
scheduler for celery (see above)

### redis
in memory database used as a messaging queue for celery; could be used to store/retreive api data, or as a cache for the backend.

### nginx
web server/load balancer/proxy for app. routes inter-container communication on host (the machine running containers) and provides user access to required services. allows public access to front end via port 80, routes user to api resources where appropriate. communication between backend/database/elasticsearch is internal and not available to a user. see deploy/nginx.conf.

## app tasks and commands

### ingesting an index - celery task from worker container
```
celery call index_data
```

### creating a superuser - python function from api
```
from client_bulksearch.db.user_utils import run_super

run_super()
```

## frontend and backend application details

more to come