Tabpanel and panel
==================

Panels are use to put components in a section. Tabpanels are a mechanism to show
and hide panels according to a panelId.

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
    The id of the panel use by tabpanel toggle if shown.

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
    Contains keys of every panelId you want to toggle if shown.

    title
        The title of the tab.

    provider
        A provider to show a number right next to the title.

components
    A list of panel objects to toggle view.

