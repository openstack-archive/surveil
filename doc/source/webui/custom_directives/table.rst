.. _webui_directives_table:

Components of a table
~~~~~~~~~~~~~~~~~~~~~

Table components represent its columns. The collumns are named after the types of cell they will contain. For example: cell-single.

Common column attributes:
*************************

All columns may define the following attributes.

title (required):
    Title of the column

class
    width of the column. Choose between xsmart, smart, medium and large

url
    Creates a link to another bansho view
   .. code-block:: javascript

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
            }



   view (required):
       the view to redirect to

   params:
       a list of objects that will be used to generate the URL

   urlParam:
       name of the url parameter

   entryKey (required):
       a key of the father inputSource’s table object. Its value is the value of the url param in the URL

cell-single
***********
Column for a specific value of the father inputSource’s table object

    .. code-block:: javascript

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

entryKey(required):
    Key of the father inputSource’s table object who’s the value is print in the column title



cell-other-fields
*****************
A column that groups values from the parent inputSource’s table object.

    .. code-block:: javascript

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

skipFields:
    Fields to exclude from the cell


cell-status-duration
********************
Only used inside a status service object table. Prints the time of the last service check
    .. code-block:: javascript

      {
          "type": "cell-status-duration",
          "attributes": {
              "title": "Duration"
          }
      }



cell-status-last-check
**********************
Only used inside a status host object table. Prints the date of the last host check
    .. code-block:: javascript

      {
          "type": "cell-status-last-check",
          "attributes": {
              "title": "Last Check"
          }
      }

cell-status-host-status
***********************
Only used inside a status host object table. Prints the host state with a specific icon for his curent state
    .. code-block:: javascript

      {
          "type": "cell-status-host-status",
          "attributes": {
              "title": "Host Status"
          }
      }

cell-status-host
****************
Only used inside a status host object table. Prints the hostName with a specific icon for his curent state
    .. code-block:: javascript

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
*************************
Only used inside a status service table. Prints a service name, its current output and an icon for his state
    .. code-block:: javascript

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
      }


cell-config-host-register
*************************
Only used inside a config host object table. Prints a validate icon if the host is register, prints an unvalidate icon if the host is not registered
    .. code-block:: javascript

      {
          "type": "cell-config-host-register",
          "attributes": {
              "title": "Register",
              "class": "xsmall"
          }
      }
