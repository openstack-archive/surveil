.. _webui_directives_actionbar:

Action Bar
==========

The action bar is the bar containing components that act on data. These
components can apply filters, recheck selected data, etc. on specified datasourceId.

.. code-block:: javascript

    {
        "type": "actionbar",
        "attributes": { "datasourceId": [ 0, 1 ] },
        "components": [...]
    }

datasourceId (required, type: array of int)
    The datasources on which the actionbar components will act.

Components
    The list of actionbar components.

Components of an actionbar
~~~~~~~~~~~~~~~~~~~~~~~~~~

Acknowledge
***********

Adds a button that will open an acknowledgement form for all selected entries. (see table checkbox attribute)

.. code-block:: javascript

  {
      "type": "actionbar-acknowledge",
      "attributes": {}
  }


Downtime
********

Adds a button that will open a downtime form for all selected entries. (see table checkbox attribute)

.. code-block:: javascript

  {
      "type": "actionbar-downtime",
      "attributes": {}
  }

Filter
******

Creates a customizable, collapsed menu of filters

.. code-block:: javascript

    {
        "type": "actionbar-filter",
        "attributes": {
        "filters": [
                {
                    "location": "componentsConfig",
                    "content": "componentsConfigFilterKey"
                }
            ]
        }
    }

location (required) [ inline || componentsConfig ]
    Where the filter is loaded. Inline will directly load content as a filter.

content (required)
    Depend on the value of location.

    +-------------------+------------------------------------------------+
    | location          | content                                        |
    +-------------------+------------------------------------------------+
    | inline            | An inline filter                               |
    +-------------------+------------------------------------------------+
    | componentsConfig  | A filters key defined on componentsConfig.json |
    +-------------------+------------------------------------------------+

More
****

Unused for the moment

Recheck
*******

Adds a recheck button that will launch a recheck command for all selected items (see table checkbox attribute)

.. code-block:: javascript

  {
      "type": "actionbar-recheck",
      "attributes": {}
  }

Search-filter
*************

Adds a search field inside actionbar that allows to search on data linked with the mother actionbar by datasourceId

.. code-block:: javascript

    {
        "type": "actionbar-search-filter",
        "attributes": {}
    }


