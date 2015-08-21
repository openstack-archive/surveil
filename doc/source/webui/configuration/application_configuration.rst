Application configuration
=========================

Application configuration is handle via ``config.json``.

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
    WebUI environment setting. Use to skip login screen in development.

username
    username use when development ``env`` is specified.

password
    password use when development ``env`` is specified.

useStoredConfig [true || false]
    If we fetch stored layout configuration from Surveil or use local.

surveilApiUrl
    Surveil Api Location.

surveilAuthUrl
    surveil Authentication Url.

refreshInterval [-1 || 1 .. infinity]
    The refresh interval for the page in second where -1 will not refresh.