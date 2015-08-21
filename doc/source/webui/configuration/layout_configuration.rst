Layout configuration
--------------------
The layout configuration is a ``JSON`` file containing the configuration of
every pages.
in a particular page the format look like this:

.. code-block:: javascript

  {
      "myPageUrl": {
          "template": "page",
          "components": [...]
    }
  }

Where the page is accessible via /#/view?view=myPageUrl.

Template [ page || dupal || drupal_dashboard ]
    This correspond to the template that will be loaded by the webUI. To

Components
    Components is an array of custom directives that define layout of the
    application. See directives (put url)

    The directive you can put are:

    * panel ./directives/panels.rst
    * tabpanel ./directives/panels.rst
    * title ./directives/title.rst
    * table ./directives/table.rst
    * actionbar ./directives/actionbar.rst

    Alternatively, you can put any custom directives but layout of the WebUI
    can look a little off.


