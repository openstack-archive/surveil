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

.. rest-controller:: surveil.api.controllers.v2.logs:LogsController
   :webprefix: /v2/status/hosts/(host_name)/events

.. rest-controller:: surveil.api.controllers.v2.logs.acknowledgements:AcknowledgementsController
   :webprefix: /v2/status/hosts/(host_name)/events/acknowledgements

.. rest-controller:: surveil.api.controllers.v2.logs.comments:CommentsController
   :webprefix: /v2/status/hosts/(host_name)/events/comments

.. rest-controller:: surveil.api.controllers.v2.logs.downtimes:DowntimesController
   :webprefix: /v2/status/hosts/(host_name)/events/downtimes

.. rest-controller:: surveil.api.controllers.v2.logs.notifications:NotificationsController
   :webprefix: /v2/status/hosts/(host_name)/events/notifications

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
