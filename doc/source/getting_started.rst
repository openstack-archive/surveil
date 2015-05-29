.. role:: bash(code)
   :language: bash

Getting Started
###############

Development environment
---------------------------

0. Prerequisite
~~~~~~~~~~~~~~~

Surveil's development environment is based on Docker and docker-compose.

First you need to install Docker refer to the project `installation documentation <https://docs.docker.com/installation/>`_

You can install docker-compose with the following command:

    :bash:`sudo pip install -U docker-compose`


1. Starting the containers
~~~~~~~~~~~~~~~~~~~~~~~~~~

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


Viewing host status
```````````````````
You can use the CLI to view the status of the currently monitored hosts and services with
:bash:`surveil status-host-list` and :bash:`surveil status-service-list`

Example output: ::

    +-------------------------------+---------------+-------+------------+-----------------------------------+
    | host_name                     | address       | state | last_check | plugin_output                     |
    +-------------------------------+---------------+-------+------------+-----------------------------------+
    | srv-ldap-01                   | 127.0.0.1     | UP    | 1431712968 | OK - 127.0.0.1: rta 0.036ms, l... |
    | sw-iwebcore-01                | 127.0.0.1     | UP    | 1431712971 | OK - 127.0.0.1: rta 0.041ms, l... |
    | os-controller-1.cloud.mtl.sfl | 145.50.1.61   | UP    | 1431713146 | OK - 172.20.1.21: rta 0.453ms,... |
    | os-compute-1.cloud.mtl.sfl    | 145.50.1.62   | UP    | 1431713144 | OK - 172.20.1.31: rta 0.318ms,... |
    | os-compute-2.cloud.mtl.sfl    | 145.50.1.63   | UP    | 1431713144 | OK - 172.20.1.32: rta 0.378ms,... |
    | os-compute-3.cloud.mtl.sfl    | 145.50.1.64   | UP    | 1431713146 | OK - 172.20.1.33: rta 0.373ms,... |
    | os-compute-4.cloud.mtl.sfl    | 145.50.1.65   | UP    | 1431713146 | OK - 172.20.1.34: rta 0.337ms,... |
    +-------------------------------+---------------+-------+------------+-----------------------------------+

You can also use the CLI to view the configured hosts in the API with
:bash:`surveil config-host-list` and :bash:`surveil config-service-list`

Adding a new host
`````````````````
The Surveil client provides function to add host

:bash:`surveil config-host-create --host_name OpenStack --address openstack.org`

This will add a new host in Surveil config, but before you can see the new host status in
the host status list with the client you need to tell Surveil that there's a new host
to monitor. Simply type:

:bash:`surveil config-reload`

It will take between 5 to 10 secondes for Surveil to tell Alignak the config
has changed. After this delay type again

:bash:`surveil status-host-list`

Using Bansho the web interface
``````````````````````````````
The Surveil client uses the Surveil API to query information concerning hosts
and services. Bansho the web interface also use this API. To use Bansho simply
open a browser  at http://localhost:8888/#/view?view=liveHosts and press login.

