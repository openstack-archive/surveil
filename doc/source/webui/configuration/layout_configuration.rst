Layout configuration
--------------------
The layout configuration is a ``JSON`` file containing the configuration of
every page.

For example, the following page would be available at: /#/view?view=myPageUrl.

.. code-block:: javascript

  {
      "myPageUrl": {
          "template": "page",
          "components": [...]
    }
  }


Template [ page || dupal || drupal_dashboard ]
    This corresponds to the template that will be loaded by the webUI.

Components
    Components is an array of custom directives that define the layout of
    the page. See directives (put url)

    The available custom directives are:

    * panel ./directives/panels.rst
    * tabpanel ./directives/panels.rst
    * title ./directives/title.rst
    * table ./directives/table.rst
    * actionbar ./directives/actionbar.rst

    Alternatively, you can use any custom directives but layout of the WebUI
    can look a little off.


