.. role:: bash(code)
   :language: bash

===============
Getting Started
===============

Developpement environnement
===========================

Surveil's developpement environnement is based on Docker and fig. There is a Makefile
at  the root of the repository with commands to make it easier to use:

* :bash:`make up`: Launch Surveil and its dependencies in containers.
* :bash:`make down`: Kill the active docker containers, if any.
* :bash:`build`: Build the surveil container.

Configuration for the different services running in the Docker container are
stored in tools/docker.
