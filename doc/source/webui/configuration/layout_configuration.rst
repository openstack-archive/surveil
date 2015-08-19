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


Template [ page || drupal || drupal_dashboard ]
    This corresponds to the template that will be loaded by the webUI.

Components
    Components is an array of custom directives that define the layout of
    the page. See :ref:`webui_custom_directives`.

    The available custom directives are:

    * :ref:`webui_directives_panels`
    * :ref:`webui_directives_title`
    * :ref:`webui_directives_table`
    * :ref:`webui_directives_actionbar`

    Alternatively, you can use any custom directives but layout of the WebUI
    can look a little off.


