# Introduction

*Bimba* is an app that allows its users to find the best route between any two points in the public transportation network of the City of Poznań (Poland).

![Build and test badge](https://github.com/wdebsqi/bimba/actions/workflows/build_test_on_pr.yml/badge.svg)
![Deploy to production badge](https://github.com/wdebsqi/bimba/actions/workflows/deploy.yml/badge.svg)
[![License badge: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# How to use bimba

Simply go to [bimba.wdebsqi.pl](http://bimba.wdebsqi.pl/) and fill out the form on the page. You need to pick the stop from which you would like to start your journey, as well as the end stop (just start typing the name of the stop and the app will suggest some for you). 

You can also specify whether you'd like to travel during the day or night.


# Architecture

The entire system is fully containerized and automated, which allows it to be run on almost any environment and work without the need for the human intervention.

The system consists of the following:

## Databases

### Neo4j

Stores the graph that represents the current state of the public transportation network:
![Network graph preview](/docs/network_graph_preview.jpg)

Nodes represent different stops and have the properties such as:
![Network graph node preview](/docs/network_graph_node_preview.jpg)

Connections store information about the lines that commute between a given two nodes:
![Network graph relationship preview](/docs/network_graph_relationship_preview.jpg)

### PostgreSQL

Used mostly for storing logs and other helpful data, such as the metadata of the already processed GTFS files (helpful for not re-processing them if the `file_parser` service restarts).

## Services

### File parser
Runs in the background and monitors the *City Transport Bureau in Poznań*'s (*Zarząd Transportu Miejskiego w Poznaniu*, in short: *ZTM*) [API](https://www.ztm.poznan.pl/pl/dla-deweloperow/index) that provides the data on the current state of the city public transportation system (such as timetables).

If it detects any changes, it fetches the GTFS files, processes them and updates the Neo4j graph.

### REST API
Provides a way of accessing the data stored in the Neo4j database via the HTTP requests. Used by the web app.

### Web app
Provides the interactive, graphical interface so that the users can find the best route between any two points in the public transportation network.

# Tech stack
The technologies used in the project include (but are not limtied to):
- [Python 3.10](https://www.python.org/) - as the programming language for the backend
- [Flask](https://flask.palletsprojects.com/) - for creating the web application and REST API's backend
- [Pandas](https://pandas.pydata.org/) - for easily processing the GTFS files provided by the ZTM
- [Sqlalchemy](https://www.sqlalchemy.org/) - for interacting with the PostgreSQL database from the backend
- HTML & CSS - for building the layout of the web app
- Javascript - for adding some interactivity to the web app


# How to set up the system on your own machine
1. [Install Docker](https://docs.docker.com/engine/install/)
1. Clone this repository
3. Navigate to the root directory of the cloned repository
4. Set up the environmental variables on your machine. They are mostly used for security reasons, so that the credentials don't leak to GitHub. Do it in the following way:

    1. create an `.env` file in the root directory of the repository and add environmental variables there. Docker will then use this file while setting up the containers.
    2. fill the file with the following environmental variables:
        - `HOST` - the IP of your machine
        - `NEO4J_USERNAME` - the name of the Neo4j database user
        - `NEO4J_PASSWORD` - password used to access the Neo4j database
        - `NEO4J_URL` - the URL used to connect to your Neo4j database (once it's up). Should have the following form: `<NEO4J_USERNAME>://<HOST>:<port>`, e.g. `mysecretusername://123.45.678.90:7687`
        - `NEO4J_AUTH` - should have the following form: `<NEO4J_USERNAME>/<NEO4J_PASSWORD>`, e.g. `mysecretusername/mysecretpassword`
        - `POSTGRES_USER` - the name of the Postgres database user
        - `POSTGRES_PASSWORD` - the password used to access the Postgres database
        - `POSTGRES_DB` - the name of the Postgres database that will store your data
        - `ZTM_FILES_DIRECTORY` - the full path to the directory on your machine, where the files downloaded from ZTM will be stored, e.g. `/home/myuser/ztm_files/`
5. Run the containers in the background: `docker compose up -d`

You can check whether everything works by running the following command: `docker ps`. You should see a total of five containers running.

You can double-check by connecting to your newly created PostgreSQL database and querying the `logs` table to see if there are any error-related logs: `SELECT * FROM logs ORDER BY created_at DESC`.

On the very first run the `file_parser` service will need to do the initial fetch and processing of the ZTM files, so it may take a while before it will be available to successfully use the components that require the Neo4j graph to exist.