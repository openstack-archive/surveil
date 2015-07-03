Surveil API
~~~~~~~~~~~

The Surveil API provides Surveil's REST API.

==================================   ==========================
**package name (RPM)**               surveil
**services**                         surveil-api.service
**Default port**                     5311
**configuration (API)**              /etc/surveil/surveil.cfg
**configuration (permissions)**      /etc/surveil/policy.json
**configuration (API - pipeline)**   /etc/surveil/api_paste.ini
==================================   ==========================

The Surveil API needs access to InfluxDB, Alignak and MongoDB. If Keystone authentication is enabled, it needs access to Keystone (see api_paste.ini).

Configuration samples
---------------------

/etc/surveil/surveil.cfg
************************

.. literalinclude:: ../../../etc/surveil/surveil.cfg

/etc/surveil/policy.json
************************

For documentation on this configuration file, refer to the OpenStack documentation.

.. literalinclude:: ../../../etc/surveil/policy.json

/etc/surveil/api_paste.ini
**************************

.. literalinclude:: ../../../etc/surveil/api_paste.ini

