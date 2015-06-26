Surveil Openstack Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~

0. Introduction : What is surveil-os-interface
----------------------------------------------

Surveil-os-interface is a daemon connected to the Openstack RabbitMQ message queue. When you create or delete an instance on Openstack, a message is send
on this queue to notify the state of the new instance (start create, end create, start delete, end delete).
The daemon subscribe to this queue and create/delete an host on surveil with information contents inside the message.

=======================  =====================================
**package name (RPM)**   surveil
**services**             surveil-os-interface.service
**configuration**        /etc/surveil/surveil_os_interface.cfg
=======================  =====================================

1. Configuration samples
------------------------
 To configure your daemon, you need a lot of information:

 * Surveil API information (URL, version, Url for authentification)
 * Openstack keystone information (URL, username, password, tenant name)
 * Openstack RabbitMQ message queue information (URL, port, username, password, name of the queue)
 * A default tag: This tag refer to a monitoring pack's name to use with our new instance.

/etc/surveil/surveil_os_interface.cfg
*************************************

.. literalinclude:: ../../../etc/surveil/surveil_os_interface.cfg