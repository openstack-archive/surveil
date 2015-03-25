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

.. rest-controller:: surveil.api.controllers.v2.status.hosts.config:ConfigController
   :webprefix: /v2/status/hosts/(host_name)/config

.. rest-controller:: surveil.api.controllers.v2.status.metrics:MetricsController
   :webprefix: /v2/status/hosts/(host_name)/metrics

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

Metrics
=======

.. rest-controller:: surveil.api.controllers.v2.status.metrics:MetricsController
   :webprefix: /v2/status/metrics

.. rest-controller:: surveil.api.controllers.v2.status.metrics:MetricController
   :webprefix: /v2/status/metrics/