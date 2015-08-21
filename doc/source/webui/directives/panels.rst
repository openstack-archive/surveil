Tabpanel and panel
==================

Panels are used to put components in a section.

Tabpanels are a mechanism to show and hide panels according to a panelId.

Panel
*****

.. code-block:: javascript

  {
      "type": "panel",
      "attributes": {
          "panelId": "mySuperPanel"
      },
      "components": [...]
  }


panelId
    The id of the panel use by tabpanel.

Components
    The list of components of the panel.

Tabpanel
********

.. code-block:: javascript

  {
     "type": "tabpanel",
     "attributes": {
         "navigation": {
             "mySuperPanel": {
                 "title": "My super panel",
                 "provider": "Provider"
             },
             "anotherPanelId": {
                 "title": "All my problems",
                 "provider": "nbProblemsProvider"
             }
         }
     },
     "components": [...]
  }

navigation (required)
    Contains keys of every panelId managed by the tabpanel.

    title
        The title of the tab.

    provider
        A provider to show a number next to the title.

components
    The list of panels managed by the tabpanel.

