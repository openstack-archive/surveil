Layout configuration
--------------------
The layout configuration is a JSON file describing every Angular components in a particular page the format look like this:

::

  {
      "[pageUrl]": {
          "template": "page",
          "components": [...]
    }
  }

Where the page is accessible via /#/view?view=PageUrl,
template is currently always page and the components is a tree containing one or many of the following items*:

- tabpanel
- panel

*You can put any directives in there including host-tree, tactical, title, actionbar

Tabpanel and panel
~~~~~~~~~~~~~~~~~~
Panels are simply a component containing thing in a styliser balise. Tabpanel contains a mechanism to show and hide panel according to there panelId.

Panel
*****

::

  {
      "type": "panel",
      "attributes": {
          "panelId": "[PanelIdKey]"
      },
      "components": [...]
  }

Attributes:

attributes:
    Contains a panelId using if the pannel is inside the components list of a tabpannel.

pannelID
    ID of the mother tabpanel. This pannel is print when you click on the mother tabpanel object

components
    A list of components print inside this panel




Tabpanel
********

::

  {
     "type": "tabpanel",
     "attributes": {
         "navigation": {
             "[firstPanelIdKey]": {
                 "title": "[title1]",
                 "provider": "[providerKey]"
             },
             "[secondPanelIdKey]": {
                 "title": "[title2]",
                 "provider": "[providerKey]"
             }
         }
     },
     "components": [...]
  }

Attributes:

navigation (required)
    Contains a panel Id associate to a title and a provider.

title
    The title print on the Web UI for the PanelIdKey object

provider
    A provider querying Surveil returning a number to print on the left of the title. See providers for key.

components
    A list of pannel objects. Must contains a panel object associate to each PannelIDKey.This pannel is print when you click on the PannelIdKey object


Components of a panel
~~~~~~~~~~~~~~~~~~~~~~

Title
*****

Title is a component who give a title to a mother object. This title can take a lot of form depending on the mother object
::

  {
   "type": "title",
   "attributes": {
       "title": [title],
       "item": [item],
       "provider": [provider]
   }
  }

Attributes:

title(required)
    the title to give at the mother object

item
    Choose a string to print inside an orange banner on the left of the title

provider
    A provider querying Surveil returning a number print inside the banner . See providers for key.

NB: The text inside a banner is : There are [provider][item] problems


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

Table
*****

::

  {
      "type": "table",
      "attributes": {
          "datasourceId": 0,
          "headerFollow": true,
          "inputSource": "contacts",
          "isWrappable": false,
          "noRepeatCell": "",
          "checkColumn": false,
          "pagingbar": true
      },
      "components": [...]
  }

Attributes:

datasourceId
    Id used by an ActionBar to interract on data

headerFollow
    The action bar follow you inside the page if you scroll down/scroll up

inputSource
    An inputSource querying Surveil returning a list of surveil objects . See inputSource for key.

isWrappable
    Unused for the moment

noRepeatCell
    Unused for the moment

checkColumn
    Add a check box collumn inside the table if activate

pagingbar
    Active/Deactive the paging bar

Components
    A list of table components
Host Tree
*********

A tree who show an host and its services like a tree.
::

  {
    "type": "host-tree",
    "attributes": {
        "inputSource": [[inputSouce1],[inputSource2]]
        ]
    }
  }

Attributes:

inputSource(required)
    An inputSource querying Surveil returning a list of surveil objects . See inputSource for key.

Container
*********

::

  {
    "type": "container",
    "components": [...]
  }

Attributes:

components
    A list of container's objects.
Text Area
*********

For the moment , this components print the configuration layout file inside a text-area . You can edit and save this configuration file

::

  {
      "type": "text-area",
      "attributes": {}
  }

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



Components of a table
~~~~~~~~~~~~~~~~~~~~~
This components are the column of our table


cell-single
***********
Collumn for a specific value of the father inputSource’s table object
::

  {
   "type": "cell-single",
   "attributes": {
       "title": "Service Description",
       "entryKey": "service_description",
       "url": {
           "view": "service",
           "params": [
               {
                   "urlParam": "host_name",
                   "entryKey": "host_name"
               },
               {
                   "urlParam": "service_description",
                   "entryKey": "service_description"
               }
           ]
       },
       "class": "medium"
   }

Attributes:

title(require):
    Title of the column

entryKey(required):
    Key of the father inputSource’s table object who’s the value is print in the column title

Url:
    A specific object to create a link on another bansho view when you click on the entryKey of a surveil object inside the table

view(require):
    the view to redirect when you click

params:
    a list of object to pass at the url to print some information on the new page

urlParam
    name of the parameter to pass to the query to obtain all information for the next page

"entryKey"(required):
    a key of the father inputSource’s table object.Its value is the value of the url param passed inside the query

class
    width of the column. Choose between smart medium and large

cell-other-fields
*****************
A column who can grouping  some value from father inputSource’s table object. You can see all this value when you clicked on the cell

::

  {
      "type": "cell-other-fields",
      "attributes": {
          "title": "Period",
          "skipFields": [
              "contact_name",
              "email",
              "host_notification_commands",
              "service_notification_commands"
          ],
          "class": "large",

      }
  }

Attributes::

title(require):
    Title of the column

skipFields:
    Key of the father inputSource’s table object value who will not print inside the column

class
    width of the column. Choose between smart medium and large


cell-status-duration

::

  {
      "type": "cell-status-duration",
      "attributes": {
          "title": "Duration"
      }
  }

Attributes::

title(require):
    Title of the column

cell-status-last-check

::

  {
      "type": "cell-status-last-check",
      "attributes": {
          "title": "Last Check"
      }
  }


cell-status-host-status

::

  {
      "type": "cell-status-host-status",
      "attributes": {
          "title": "Host Status"
      }
  }

cell-status-host

::
{
                                        "type": "cell-status-host",
                                        "attributes": {
                                            "title": "Hosts",
                                            "url": {
                                                "view": "host",
                                                "params": [
                                                    {
                                                        "urlParam": "host_name",
                                                        "entryKey": "host_host_name"
                                                    }
                                                ]
                                            }
                                        }
                                    }

cell-status-service-check

{
                                        "type": "cell-status-service-check",
                                        "attributes": {
                                            "title": "Service Check",
                                            "url": {
                                                "view": "service",
                                                "params": [
                                                    {
                                                        "urlParam": "host_name",
                                                        "entryKey": "host_host_name"
                                                    },
                                                    {
                                                        "urlParam": "service_description",
                                                        "entryKey": "service_service_description"
                                                    }
                                                ]
                                            }
                                        }
                                    },


cell-config-host-register
{
                                "type": "cell-config-host-register",
                                "attributes": {
                                    "title": "Register",
                                    "class": "xsmall"
                                }
                            }
Components of a container
~~~~~~~~~~~~~~~~~~~~~~~~~