Action Bar
==========

The action bar is the bar containing components that act on data. Theses
components can apply filters, recheck selected data, etc.

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

Open the acknowledge form that is apply on selected entries. (see table checkbox attribute)

.. code-block:: javascript

  {
      "type": "actionbar-acknowledge",
      "attributes": {}
  }


Downtime
********

Open the downtime form that is apply on selected entries. (see table checkbox attribute)

.. code-block:: javascript

  {
      "type": "actionbar-downtime",
      "attributes": {}
  }

Filter
******

Create a collapse menu of filters

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

Implemented but unused for the moment

Recheck
*******

Make recheck on objects selected with a checkbox (see table checkbox attribute)

.. code-block:: javascript

  {
      "type": "actionbar-recheck",
      "attributes": {}
  }

Search-filter
*************

Add a search field inside actionbar on data linked with the mother actionbar by datasourceId

.. code-block:: javascript

    {
        "type": "actionbar-search-filter",
        "attributes": {}
    }


