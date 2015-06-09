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

You should be able to test your modification by accessing ``http://localhost:8080/v2/hello`` with your browser.

Disabling permissions
~~~~~~~~~~~~~~~~~~~~~

Depending on what you are working on, it might be practical to disable permissions. This can be done by editing the ``policy.json`` file found at ``etc/surveil/policy.json``.

For example, you could modify the following line: ::

        "surveil:admin": "rule:admin_required",

by: ::

    "surveil:admin": "rule:pass",

This will modify permissions so that all API calls that require the ``admin`` rule now pass without any verification.
