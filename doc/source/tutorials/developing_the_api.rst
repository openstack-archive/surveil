.. role:: bash(code)
   :language: bash

Developping the API
-------------------

Launching the stack
~~~~~~~~~~~~~~~~~~~

If you have completed the :ref:`tutorial_getting_started` tutorial, you should know how to launch the stack: ::

    sudo docker-compose up

Editing the code
~~~~~~~~~~~~~~~~

The Surveil container mounts your local project folder and pecan reloads every time the project files change thus providing a proper development environment.

For example, edit the ``surveil/api/controllers/v2/hello.py`` file and change ``Hello World!`` by ``Hello Devs!``.

After you save the file, the following logs will appear in Surveil's output: ::

    surveil_1  | Some source files have been modified
    surveil_1  | Restarting server...

You should be able to test your modification by accessing ``http://localhost:5311/v2/hello`` with your browser.

Disabling permissions
~~~~~~~~~~~~~~~~~~~~~

Depending on what you are working on, it might be practical to disable permissions. This can be done by editing the ``policy.json`` file found at ``etc/surveil/policy.json``.

For example, you could modify the following lines: ::

    "admin_required": "role:admin or is_admin:1",
    "surveil_required": "role:surveil or rule:admin_required",

    "surveil:admin": "rule:admin_required",
    "surveil:authenticated": "rule:surveil_required",

by: ::

    "admin_required": "@",
    "surveil_required": "@",

    "surveil:admin": "@",
    "surveil:authenticated": "@",

This will modify permissions so that all API calls that require the ``admin`` rule now pass without any verification.


Developping the API without docker
----------------------------------

You can get development environment without docker

::

    git clone https://review.openstack.org/stackforge/surveil￼
    cd surveil
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py develop
    python setup.py install_data
    surveil-api -p env/etc/surveil/config.py -a env/etc/surveil/api_paste.ini -c env/etc/surveil/surveil.cfg -r

Edit your config files

::

    vim env/etc/surveil/config.py
    vim env/etc/surveil/surveil.cfg
    vim env/etc/surveil/policy.json
    vim env/etc/surveil/api_paste.ini

Don't forget to start your databases (MongoDB and InfluxDB)
