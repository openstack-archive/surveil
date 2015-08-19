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
