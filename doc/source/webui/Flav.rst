Surveil Web UI
--------------


Tabpanel and panel
~~~~~~~~~~~~~~~~~~
Panels are simply a component containing thing in a styliser balise. Tabpanel contains a mechanism to show and hide panel according to there panelId.

Panel
*****

Tabpanel
********

.. code-block:: javascript
    {
       "type": "tabpanel",
       "attributes": {
           "navigation": {
               "[firstPanelIdKey]": {
                   "title": "[title1]",
                   "provider": "providerKey"
               },
               "[secondPanelIdKey]": {
                   "title": "[title2]",
                   "provider": "providerKey"
               }
           }
       },
       "components": [...]
    }

Attributes:

navigation (required)
    contains a panel Id associate to a title and a provider.

title
    the title print on the Web UI for the PanelIdKey object

provider
    a provider querying Surveil returning a number to print on the left of the title. See providers for key.

components
    Must contains a panel object associate to each PannelIDKey.This pannel is print when you click on the PannelIdKey object
