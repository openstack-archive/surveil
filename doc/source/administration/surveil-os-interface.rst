Surveil Openstack Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~

surveil-os-interface is a daemon that connects to the OpenStack message queue. It reacts to various events and automatically configures Surveil monitoring. For example, instances created in Nova will automatically be monitored by Surveil.

=======================  =====================================
**package name (RPM)**   surveil
**services**             surveil-os-interface.service
**configuration**        /etc/surveil/surveil_os_interface.cfg
=======================  =====================================

Surveil-os-interface needs acces to OpenStack's message queue. The following options must be set in ``/etc/nova/nova.conf``: ::

     notification_driver=nova.openstack.common.notifier.rpc_notifier
     notification_topics=notifications,surveil
     notify_on_state_change=vm_and_task_state
     notify_on_any_change=True

Configuration samples
---------------------

/etc/surveil/surveil_os_interface.cfg
*************************************

.. literalinclude:: ../../../etc/surveil/surveil_os_interface.cfg
