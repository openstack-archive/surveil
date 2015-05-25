.. docbookrestapi

======
Status
======

.. rest-controller:: surveil.api.controllers.v2.status:StatusController
   :webprefix: /v2/status


Hosts
=====

.. rest-controller:: surveil.api.controllers.v2.status.hosts:HostsController
   :webprefix: /v2/status/hosts

.. rest-controller:: surveil.api.controllers.v2.status.hosts:HostController
   :webprefix: /v2/status/hosts/

.. rest-controller:: surveil.api.controllers.v2.status.hosts:ConfigController
   :webprefix: /v2/status/hosts/(host_name)/config

.. rest-controller:: surveil.api.controllers.v2.status.hosts:HostCheckResultsSubController
   :webprefix: /v2/status/hosts/(host_name)/results

.. rest-controller:: surveil.api.controllers.v2.status.hosts:ServiceCheckResultsSubController
   :webprefix: /v2/status/hosts/(host_name)/services/(service_description)/results

.. rest-controller:: surveil.api.controllers.v2.status.events:EventsController
   :webprefix: /v2/status/events/


Services
========

.. rest-controller:: surveil.api.controllers.v2.status.services:ServicesController
   :webprefix: /v2/status/services


types documentation
===================

.. autotype:: surveil.api.datamodel.status.live_service.LiveService
   :members:

.. autotype:: surveil.api.datamodel.status.live_host.LiveHost
   :members:

.. autotype:: surveil.api.datamodel.status.live_query.LiveQuery
   :members:

.. autotype:: surveil.api.datamodel.status.event.Event
   :members:
