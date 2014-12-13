.. role:: bash(code)
   :language: bash

===============
Getting Started
===============

Developpement environnement
===========================

Surveil's developpement environnement is based on Docker. There is a Makefile
at  the root of the repository with commands to make it easier to use:

* :bash:`make docker_run`: Launch Surveil inside a container in non-interactive mode.
* :bash:`make docker_run_interactive`: Launch Surveil inside a container in interactive mode. You will have to start the services yourself.
* :bash:`make docker_kill`: Kill the active docker containers, if any.

Configuration for the different services running in the Docker container are
stored in tools/docker.
