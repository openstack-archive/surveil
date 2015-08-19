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

env [production || development]
    WebUI environment setting to skip login screen in development.

username
    username use when development env is specified.

password
    password use when development env is specified.

useStoredConfig [true || false]
    If we fetch stored layout configuration from Surveil or use local.

surveilApiUrl
    Surveil Api Location.

surveilAuthUrl
    surveil Authentication Url.

refreshInterval [-1 || 1 .. infinity]
    The refresh interval in second where -1 is no refresh.
