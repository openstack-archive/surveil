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
Surveil ships with configuration templates (or packs). While it is possible possible to define services by yourself, it is suggested
to use configuration templates. For example, the following command defines a host using the OpenStack Keystone template: ::

    surveil config-host-create --host_name os-controller-1.cloud.mtl.sfl --address 172.20.1.21 --use linux-keystone --custom_fields '{"_OS_AUTH_URL":"http://145.50.1.61:5000/v2.0", "_OS_TENANT_NAME":"admin", "_OS_USERNAME":"admin", "_OS_PASSWORD":"password","_KS_SERVICES":"identity"}'

This will create a ``os-controller-1.cloud.mtl.sfl`` host using the ``linux-keystone`` template. A service will be automatically
defined to monitor the Keystone API with the authentication credentials provided. More documentation about configuration packs
is available `here <http://sfl-monitoring-tools.readthedocs.org>`_.
