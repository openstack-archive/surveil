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

Services
========

.. rest-controller:: surveil.api.controllers.v2.config.services:ServicesController
   :webprefix: /v2/config/services

.. autotype:: surveil.api.datamodel.config.service.Service
   :members:


Commands
========

.. rest-controller:: surveil.api.controllers.v2.config.commands:CommandsController
   :webprefix: /v2/config/commands

.. rest-controller:: surveil.api.controllers.v2.config.commands:CommandController
   :webprefix: /v2/config/commands

Business impact modulations
===========================

.. rest-controller:: surveil.api.controllers.v2.config.businessimpactmodulations:BusinessImpactModulationsController
   :webprefix: /v2/config/businessimpactmodulations

Check modulations
===========================

.. rest-controller:: surveil.api.controllers.v2.config.checkmodulations:CheckModulationsController
   :webprefix: /v2/config/checkmodulations

Notification ways
=================

.. rest-controller:: surveil.api.controllers.v2.config.notificationways:NotificationWaysController
   :webprefix: /v2/config/notificationways

types documentation
===================

.. autotype:: surveil.api.datamodel.config.command.Command
   :members:

.. autotype:: surveil.api.datamodel.config.host.Host
   :members:

.. autotype:: surveil.api.datamodel.checkresult.CheckResult
   :members:

.. autotype:: surveil.api.datamodel.config.businessimpactmodulation.BuisnessImpactModulation
   :members:

.. autotype:: surveil.api.datamodel.config.checkmodulation.CheckModulation
   :members:

.. autotype:: surveil.api.datamodel.config.notificationway.NotificationWay
   :members:
