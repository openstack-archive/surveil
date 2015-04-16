.. role:: bash(code)
   :language: bash

Surveil
=======

Monitoring as a Service

An OpenStack related project designed to provide highly available, scalable
and flexible monitoring for OpenStack.

Project Info
############

 * Wiki: https://wiki.openstack.org/wiki/Surveil
 * IRC: #surveil at freenode
 * Documentation: https://surveil.readthedocs.org/
 * Open Gerrit Changesets: https://review.openstack.org/#/q/status:open+surveil,n,z

Getting Started
###############

Developpement environnement
---------------------------

Surveil's developpement environnement is based on Docker and docker-compose.

You can install docker-compose with the following command:

    :bash:`sudo pip install -U docker-compose`

You will then be able to use the environment with the following commands:

* :bash:`sudo docker-compose up`: Launch Surveil and its dependencies in containers.
* :bash:`sudo docker-compose down`: Kill the active docker containers, if any.
* :bash:`sudo docker-compose rm`: Remove all containers, if any.
* :bash:`sudo docker-compose`: Build the docker images.

Configuration for the different services running in the Docker containers are
stored in tools/docker.

After running :bash:`sudo docker-compose up`, you should be able to acces all
services at the ports configured in the docker-compose.yml file.

* Surveil API: http://localhost:8080/v1/hello
* InfluxDB: http://localhost:8083
* Grafana: http://localhost:80/grafana
* Shinken WebUI: http://localhost:7767/all

The Surveil container mounts your local project folder and pecan reloads every
time the project files change thus providing a proper development environment.
