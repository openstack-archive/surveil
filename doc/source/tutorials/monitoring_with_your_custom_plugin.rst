.. role:: bash(code)
   :language: bash

Monitoring with your custom plugin
##################################

Surveil is compatible with Nagios plugins. It is trivial to write a custom plugin to monitor your applcation. In this guide, we will create a new plugin and configure a new Host that uses it in Surveil.

1. Test the check_example plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step to create a plugin is to successfully test the check_example plugin. This plugin
will serve as a base file to create your own plugin.

Create virtual environment and install requirements: ::

    virtualenv env
    source env/bin/activate
    cd tools/docker/alignak_container/plugins/check-example
    pip install -r requirements.txt

Install the check_example plugin: ::

    python setup.py develop

Run the plugin: ::

    check_example

The output should look like this: ::

    DISK OK - free space: / 3326 MB (56%); | /=2643MB;5948;5958;0;5968

2. Modify the plugin
~~~~~~~~~~~~~~~~~~~~

The next step is to modify the plugin to meet your needs. In order to do this,
please refer to the `Nagios plugin API documentation <http://nagios.sourceforge.net/docs/3_0/pluginapi.html>`_.


3. Create a host using this plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that you are done developing your plugin, it is time to use it in Surveil.

Creating a command
------------------

Before you can use your plugin in a host/service configuration, you need to create an Alignak command: ::

    surveil config-command-create --command_name check_example --command_line "check_example"

Creating a host
---------------

Create a host with the following command: ::

   surveil config-host-create --host_name check_example_host --address savoirfairelinux.com

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
