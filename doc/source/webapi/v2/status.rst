.. docbookrestapi

======
Status
======

.. rest-controller:: surveil.api.controllers.v2.status.status:StatusController
   :webprefix: /v2/status


Events
======

.. rest-controller:: surveil.api.controllers.v2.status.events.events:EventsController
:webprefix: /v2/status/events/


Hosts
=====

.. rest-controller:: surveil.api.controllers.v2.status.hosts.hosts:HostsController
   :webprefix: /v2/status/hosts

.. rest-controller:: surveil.api.controllers.v2.status.hosts.hosts:HostController
   :webprefix: /v2/status/hosts/

.. rest-controller:: surveil.api.controllers.v2.status.hosts.hosts:ConfigController
   :webprefix: /v2/status/hosts/(host_name)/config

.. rest-controller:: surveil.api.controllers.v2.status.hosts.results:CheckResultsSubController
   :webprefix: /v2/status/hosts/(host_name)/results

.. rest-controller:: surveil.api.controllers.v2.status.hosts.metrics:MetricsController
   :webprefix: /v2/status/hosts/(host_name)/metrics

.. rest-controller:: surveil.api.controllers.v2.status.hosts.metrics:MetricController
   :webprefix: /v2/status/hosts/(host_name)/metrics

.. rest-controller:: surveil.api.controllers.v2.status.hosts.services.results:CheckResultsSubController
   :webprefix: /v2/status/hosts/(host_name)/services/(service_description)/results

.. rest-controller:: surveil.api.controllers.v2.status.hosts.services.metrics:MetricsController
   :webprefix: /v2/status/hosts/(host_name)/services/(service_description)/metrics


Services
========

.. rest-controller:: surveil.api.controllers.v2.status.services.services:ServicesController
   :webprefix: /v2/status/services


types documentation
===================

.. autotype:: surveil.api.datamodel.status.live_service.LiveService
   :members:

.. autotype:: surveil.api.datamodel.status.live_host.LiveHost
   :members:

.. autotype:: surveil.api.datamodel.status.live_query.LiveQuery
   :members:

.. autotype:: surveil.api.datamodel.status.metrics.metric.Metric
   :members:

.. autotype:: surveil.api.datamodel.status.metrics.time_interval.TimeInterval
   :members:

.. autotype:: surveil.api.datamodel.status.event.Event
   :members:

