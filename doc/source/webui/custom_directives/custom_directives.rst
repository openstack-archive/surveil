.. _webui_custom_directives:

Custom directives
=================

Custom directives are use in WebUI mainly to create complex page layout.

All injectable directives in a layout configuration file are found in
```app/components/custom_directive/``` and have two properties: Attributes and
Components.

Attributes
    Attributes are used to configure the current directive.

    For example, in the table directive, we use attributes to specify the shown datasourceId,
    whether the table header will follow on scroll and whether there is a checkbox column.

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
    Components is a list of directives to inject in the current directive.
    For example, in the table directive, we use components to specify columns.

.. code-block:: javascript

    {
        "type": "table",
        "attributes": {...},
        "components": [
            {
                "type": "cell-host-state",
                "attributes": {...}
            },
            {
                "type": "cell-service-state",
                "attributes": {...}
            }
        ]
    }
