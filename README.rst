.. role:: bash(code)
   :language: bash

Surveil
=======

Monitoring as a Service

An OpenStack related project designed to provide highly available, scalable
and flexible monitoring for OpenStack.

Check the `live demo <http://surveil.savoirfairelinux.net/>`_ of the web interface.

Global project architecture
###########################

.. image:: https://github.com/stackforge/surveil-specs/raw/master/surveil_architecture.png
   :height: 2400px
   :width: 800px
   :alt: Surveil software architecture
   :align: center

Main components
###############

* `Surveil <https://github.com/stackforge/surveil>`_: REST API
* `python-surveilclient <https://github.com/stackforge/python-surveilclient>`_: command line interface and Python library
* `Alignak <https://github.com/Alignak-monitoring/alignak>`_: Core monitoring framework
* `Bansho <https://github.com/stackforge/bansho>`_: Surveil web interface
* `InfluxDB <https://github.com/influxdb/influxdb>`_: Storing metrics
* `Redis <http://redis.io/>`_: API caching
* `Grafana <http://grafana.org/>`_: Data visualization

Project Info
############

* Documentation: https://surveil.readthedocs.org/
* IRC: #surveil at freenode
* Wiki: https://wiki.openstack.org/wiki/Surveil
* Open Gerrit Changesets: https://review.openstack.org/#/q/status:open+surveil,n,z
* Bug tracker: https://bugs.launchpad.net/surveil
* Bansho (Surveil Web UI): https://github.com/stackforge/bansho
* Puppet module: https://github.com/stackforge/puppet-surveil


Getting started
###############

There is a getting started guide available `here <https://surveil.readthedocs.org/en/latest/getting_started.html>`_.
