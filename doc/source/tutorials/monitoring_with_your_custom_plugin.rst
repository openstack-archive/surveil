.. role:: bash(code)
   :language: bash

Monitoring with your custom plugin
##################################

Surveil is compatible with Nagios plugins. It is trivial to write a custom plugin to monitor your applcation. In this guide, we will create a new plugin and configure a new Host that uses it in Surveil.

0. Install the plugin
~~~~~~~~~~~~~~~~~~~~~

Surveil support Nagios plugins. For more information about Nagios plugins, please refer to the `Nagios plugin API documentation <http://nagios.sourceforge.net/docs/3_0/pluginapi.html>`_ for more information.

There are many plugins available on the web. For example, the `nagios-plugins <https://github.com/nagios-plugins/nagios-plugins>`_ project contains many plugins written in C and the `monitoring-tools <https://github.com/savoirfairelinux/monitoring-tools>`_ project contains many plugins written in Python.

Surveil loads plugins from ``/usr/lib/monitoring/plugins/``. In this example, we will be installing  a simple fake plugin written in Bash: ::

    echo -e '#!/bin/bash\necho "DISK $1 OK - free space: / 3326 MB (56%); | /=2643MB;5948;5958;0;5968"' | sudo tee /usr/lib/monitoring/plugins/custom/check_example
    chmod +x /usr/lib/monitoring/plugins/custom/check_example

1. Create a host using this plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that you are done developing your plugin, it is time to use it in Surveil.

Creating a command
------------------

Before you can use your plugin in a host/service configuration, you need to create an Alignak command: ::

    surveil config-command-create --command_name check_example --command_line '$CUSTOMPLUGINSDIR$/check_example $HOSTADDRESS$'

Creating a host
---------------

Create a host with the following command: ::

   surveil config-host-create --host_name check_example_host --address savoirfairelinux.com --use generic-host

Creating a Service
------------------

Create a service with the following command: ::

    surveil config-service-create --host_name check_example_host --service_description check_example_service --check_command "check_example" --max_check_attempts 4 --check_interval 5 --retry_interval 3 --check_period "24x7" --notification_interval 30 --notification_period "24x7" --contacts admin --contact_groups admins

Reload the config
-----------------

Reload the config this will tell Alignak to reload the new config with the new host ::

    surveil config-reload

Show the new service
--------------------

Show the service list with this command: ::

    surveil status-service-list


You should see the service you just add in the list with the correct status (this could take a minute a two for the
result to show)
