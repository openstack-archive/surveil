.. role:: bash(code)
   :language: bash

Getting Started
###############

Developpement environnement
---------------------------

1. Starting the containers
~~~~~~~~~~~~~~~~~~~~~~~~~~

Surveil's developpement environnement is based on Docker and docker-compose.

You can install docker-compose with the following command:

    :bash:`sudo pip install -U docker-compose`

You will then be able to use the environment with the following commands:

* :bash:`sudo docker-compose up`: Launch Surveil and its dependencies in containers.
* :bash:`sudo docker-compose down`: Kill the active docker containers, if any.
* :bash:`sudo docker-compose rm`: Remove all containers, if any.
* :bash:`sudo docker-compose build`: Build the docker images.

Configuration for the different services running in the Docker containers are
stored in tools/docker.

After running :bash:`sudo docker-compose up`, you should be able to acces all
services at the ports configured in the docker-compose.yml file.

* Surveil API: http://localhost:8080/v1/hello
* Bansho (surveil web interface): http://localhost:8888 (any login info is fine)
* InfluxDB: http://localhost:8083 (user:root pw:root)
* Grafana: http://localhost:80 (user:admin pw:admin)
* Shinken WebUI: http://localhost:7767/all (user:admin pw:admin)

After about 40 seconds, a script will be executed to create fake hosts in the
Surveil configuration. You should see it in the docker-compose logs.

The Surveil container mounts your local project folder and pecan reloads every
time the project files change thus providing a proper development environment.

**Note**: Fedora users might want to uncomment the :bash:`privileged: true` line in `docker.compose.yml` if they face permissions issues.

2. Interacting with the API
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the `python-surveilclient <https://pypi.python.org/pypi/python-surveilclient>`_ CLI to interact with the API.

Install it with the following command:

    :bash:`sudo pip install -U python-surveilclient`

You'll need to provide the Surveil API URL. You can do this with the
``--surveil-api-url`` parameter, but its easier to just set it as environment
variable::

    export SURVEIL_API_URL=http://localhost:8080/v2
    export SURVEIL_AUTH_URL=http://localhost:8080/v2/auth


You can now use the CLI to view the status of the currently monitored hosts:

    :bash:`surveil status-host-list`

