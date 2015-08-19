Components configuration
========================

Components configuration manage some of the basic configuration of directives
injected in the application.

The components config is divided in two parts: filters and inputSource.

.. code-block:: javascript

    {
        "filters": {...},
        "inputSource": {...}
    }

Filters
-------

Filters define query ``POST`` to Surveil to retrieve specific data.

.. code-block:: javascript

    "hostOk": {
        "name": "All Ok",
        "filter": {
            "hosts": {
                "is": {
                    "state": [
                        "UP"
                    ]
                }
            }
        }
    }

FilterKey (hostOk)
    The key of the filter.

Name
    The name of the filter use when selecting filters in actionbar-filter

Filter
    A surveil query that will be pass a the data of a post to Surveil. Refer to Surveil Query documentation.


InputSource
-----------

Input source in components configuration represent

.. code-block:: javascript

  "hostOpenProblems": {
      "provider": "status",
      "endpoint": "hosts",
      "filter": "hostOk"
  }

In this example the Surveil url to be query will be: status/hosts/

Provider [ "config" || "status" || ... ]
    Which kind of objects the WebUi will query Surveil.

Endpoint [ "hosts" || "service" || "commands" || .. ]
    The type of objects the WebUi will query Surveil.

Filter
    The filter key specified in filters.
