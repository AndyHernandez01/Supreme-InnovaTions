# Supreme-InnovaTions
IoT connectivity for Biosure Devices

#Requirements
* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).

All python packages and environments are automatically managed my Python-Poetry

* Start with docker-compose build:
This will install all necesarry images for the containers
'''bash
docker-compose build
'''
* Now run Docker Compose to start the stack
'''bash
docker-compose up -d
'''

*You can now interact with the API through HTTP calls (curl) or localhost:8000/docs

##To change Database:
Modify SQLAlchemy Models in './backend/app/app/models', and schemas in ./backend/app/schemas
