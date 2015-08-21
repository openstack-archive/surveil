Tabpanel and panel
~~~~~~~~~~~~~~~~~~

Panels are use to put components in a section. Tabpanels are a mechanism to show
and hide panel according to there panelId.

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
    The id of the panel use by tabpanel to toggle if shown.

Components
    The list of components of the panel

Tabpanel
********

.. code-block:: javascript

  {
     "type": "tabpanel",
     "attributes": {
         "navigation": {
             "mySuperPanel": {
                 "title": "My super panel",
                 "provider": "[providerKey]"
             },
             "anotherPanelId": {
                 "title": "Another panel",
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

