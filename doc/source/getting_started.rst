.. role:: bash(code)
   :language: bash

===============
Getting Started
===============

Developpement environnement
===========================

Surveil's developpement environnement is based on Docker and docker-compose.

You can install docker-compose with the following command:

    :bash:`sudo pip install -U docker-compose`

You will then be able to use the environment with the following commands:

* :bash:`docker-compose up`: Launch Surveil and its dependencies in containers.
* :bash:`docker-compose down`: Kill the active docker containers, if any.
* :bash:`docker-compose rm`: Remove all containers, if any.
* :bash:`docker-compose`: Build the docker images.

Configuration for the different services running in the Docker container are
stored in tools/docker.

The Surveil container mounts your local project folder and pecan reloads every
time the project files change thus providing a proper development environment.
