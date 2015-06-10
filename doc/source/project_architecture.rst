Surveil project architecture
============================

Global project architecture
###########################

.. image:: https://github.com/stackforge/surveil-specs/raw/master/surveil_architecture.png
   :height: 2400px
   :width: 800px
   :alt: Surveil software architecture
   :align: center

OpenStack Integration
#####################

.. image:: https://github.com/stackforge/surveil-specs/raw/master/surveil_architecture_with_openstack.png
   :height: 2400px
   :width: 800px
   :alt: Surveil software architecture with OpenStack
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
