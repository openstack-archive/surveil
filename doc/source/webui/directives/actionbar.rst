Action Bar
**********

Action Bar is a bar container with components who can filters, reload, search data. This data are inside the mother object and can be identified by a datasourceId
::

  {
    "type": "actionbar",
    "attributes": { "datasourceId": [ [DTID1], [DTID2]]},
    "components": [...]
  }


Attributes:

datasourceId (required, type: array of int)
    The datasources on which the actionbar components will act.

Components
    A list of actionbar components.

Components of an actionbar
~~~~~~~~~~~~~~~~~~~~~~~~~~

Acknowledge
***********

Open a form to make an acknowledge on objects selected with a checkbox (see table checkbox attribute)
::

  {
      "type": "actionbar-acknowledge",
      "attributes": {}
  }


Down time
*********

Open a form to make a downtime on objects selected with a checkbox (see table checkbox attribute)
::

  {
      "type": "actionbar-downtime",
      "attributes": {}
  }

filter
******

Create a collapse menu of filters
::

  {
      "type": "actionbar-filter",
      "attributes": {
          "filters": [{
                        "location": [locationkey],
                        "content": [contentKey]
                     }]
      }
  }

Attributes:

location(required)
    2 key available : inline and componentsConfig.

content(required)
    depend on the value of location. If inside, content is a live query object used to filter a data
    If it is componentsConfig, content must refer to a filters object defined on componentsConfig.json. The filters of this object is used to filter data
more
****
Implemented but unused for the moment

recheck
*******
Make recheck on objects selected with a checkbox (see table checkbox attribute)
::

  {
      "type": "actionbar-recheck",
      "attributes": {}
  }

search-filter
*************
Add a search field inside actionbar on data linked with the mother actionbar by datasourceId
::

  {
      "type": "actionbar-search-filter",
      "attributes": {}
  }


