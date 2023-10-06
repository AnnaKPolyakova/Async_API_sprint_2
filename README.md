# Sprint 5 project work

Creates indexes person, genre and fills with data from the postgres database
(run via db_updater.py in a separate container)
API for receiving data from es about films, persons, genres

Technologies and requirements:
```
Python 3.9+
Fast API
```

### Docker Settings

##### Installation

* [Detailed installation guide](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### Docker-compose settings

##### Installation

* [Detailed Installation Guide](https://docs.docker.com/compose/install/)

### Launch the application

#### Before starting the project, create environment variables
Create a .env in the root and add the necessary variables to it
Example in .env.example - to run the entire application in docker
Example in .env.example-local - to run the application locally and partially in docker

#### Running a project entirely in docker containers

* `docker-compose up --build`

Documentation at:
http://0.0.0.0/api/openapi
API:
http://0.0.0.0/api/v1/....


To stop the container:
* `docker-compose down --rmi all --volumes`

#### Running the project partially in docker containers (redis and elastic)

* `docker-compose -f docker-compose-local.yml up --build`
* `python src/main.py`
* `python -m src.etl.db_updater`

Documentation at:
http://0.0.0.0:8000/api/openapi
API:
http://0.0.0.0:8000/api/v1/....

To stop the container:
* `docker-compose -f docker-compose-local.yml down --rmi all --volumes`

### Testing

Create a file called .env_test in the tests/functional folder and add it to it
necessary variables
Example in .env_test.example - to run entire tests in docker
Example in .env_test.example - local - to run tests locally and
partially in docker


#### Running tests in a docker container

* `docker-compose -f tests/functional/docker-compose-test.yml up --build`

To stop the container:
* `docker-compose -f tests/functional/docker-compose-test.yml down --rmi all`

#### Running tests partially in a docker container

* `docker-compose -f tests/functional/docker-compose-test-local.yml up --build`
* `pytest tests/functional/src`

To stop the container:
* `docker-compose -f tests/functional/docker-compose-test-local.yml down --rmi all`
