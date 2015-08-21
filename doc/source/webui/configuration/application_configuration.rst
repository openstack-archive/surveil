Application configuration
=========================

Application configuration is found in ``config.json``.

.. code-block:: javascript

   {
      "env": "production",
      "username": "myDevUsername",
      "password": "myDevPassword",
      "useStoredConfig": true
      "surveilApiUrl": "surveil/v2",
      "surveilAuthUrl": "surveil/v2/auth",
      "refreshInterval": -1
   }

env (required) [production || development]
    WebUI environment setting. Used to skip login page in development.

username
    username used when development ``env`` is specified.

password
    password used when development ``env`` is specified.

useStoredConfig [true || false]
    Whether to fetch stored layout configuration from Surveil or to use local.

surveilApiUrl
    Surveil API URL.

surveilAuthUrl
    Surveil Auth URL.

refreshInterval [-1 || 1 .. infinity]
    The refresh interval for the page in second where -1 will not refresh.