Custom directives
=================

Custom directives are use in WebUi mainly to create complex page layout with a
JSON configuration file.

Every injectable directives in a layout configuration file are found in
```app/components/directive/``` and have three properties: Attributes and
Components.

Attributes
    Attributes are use to configure current directive for example in the
    table directive we use attributes to specify, among other things, the
    datasourceId, if the table header will follow on scroll and if there is a
    checkbox column.

.. code-block:: javascript

    {
        "type": "table",
        "attributes": {
            "datasourceId": 0,
            "headerFollow": true,
            "inputSource": "configServices",
        },
        "components": [...]
    }


Components
    Components on the other hand are where we specify all the others directives
    you want to inject in the current directive. For example, in the table
    directive we use components to specify columns.

.. code-block:: javascript

    {
        "type": "table",
        "attributes": {...},
        "components": [
            {
                "type": "cell-single",
                "attributes": {...}
            },
            {
                "type": "cell-other-fields",
                "attributes": {...}
            }
        ]
    }
