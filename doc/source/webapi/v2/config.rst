.. docbookrestapi

======
Config
======

.. rest-controller:: surveil.api.controllers.v2.config:ConfigController
   :webprefix: /v2/config

Hosts
=====

.. rest-controller:: surveil.api.controllers.v2.config.hosts:HostsController
   :webprefix: /v2/config/hosts

.. rest-controller:: surveil.api.controllers.v2.config.hosts:HostController
   :webprefix: /v2/config/hosts

.. rest-controller:: surveil.api.controllers.v2.config.hosts:HostServicesSubController
   :webprefix: /v2/config/hosts/(host_name)/services

.. rest-controller:: surveil.api.controllers.v2.config.hosts:HostServiceSubController
   :webprefix: /v2/config/hosts/(host_name)/services/(service_name)

.. rest-controller:: surveil.api.controllers.v2.config.hosts:HostCheckResultsSubController
   :webprefix: /v2/config/hosts/(host_name)/results

.. rest-controller:: surveil.api.controllers.v2.config.hosts:ServiceCheckResultsSubController
   :webprefix: /v2/config/hosts/(host_name)/services/(service_description)/results

.. autotype:: surveil.api.controllers.v2.datamodel.checkresult.CheckResult
   :members:

.. autotype:: surveil.api.controllers.v2.datamodel.host.Host
   :members:

Services
========

.. rest-controller:: surveil.api.controllers.v2.config.services:ServicesController
   :webprefix: /v2/config/services

.. autotype:: surveil.api.controllers.v2.datamodel.service.Service
   :members:


Commands
========

.. rest-controller:: surveil.api.controllers.v2.config.commands:CommandsController
   :webprefix: /v2/config/commands

.. rest-controller:: surveil.api.controllers.v2.config.commands:CommandController
   :webprefix: /v2/config/commands

.. autotype:: surveil.api.controllers.v2.datamodel.command.Command
   :members:

