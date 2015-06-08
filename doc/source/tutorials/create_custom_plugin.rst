.. role:: bash(code)
   :language: bash

Create custom plugin
########################

If you want to do specific check on your hosts or services you will need to install create an
Nagios plugin to do please follow theses steps:

1. Test check_example plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step to create a plugin is to successfully test the check_example plugin. This plugin
will serve as a base file to create your own plugin.

Create virtual environment en install requirements.

    :bash:`cd surveil`
    :bash:`virtualenv env`
    :bash:`source env/bin/activate`
    :bash:`pip install -r requirements.txt -r test-requirements.txt`

Install check_example plugin.

    :bash:`cd tools/docker/alignak_container/plugins/check-example`
    :bash:`python setup.py develop`

Run the plugin.

    :bash:`check_example`

2. Modify the plugin
~~~~~~~~~~~~~~~~~~~~

The next step is to modify the plugin to meet your need to do this
please refer to the `Alignak plugin documentation <http://alignak.readthedocs.org/en/latest/15_development/pluginapi.html>`_


3. Create an host using this plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have tested your plugin and are satisfied start the Surveil development environments
with:

   :bash:`sudo docker-compose up`

After that you will add an host using the new plugin with this command:

   :bash:`surveil config-host-create --host_name checkExample --address savoirfairelinux.com --use check_example`

