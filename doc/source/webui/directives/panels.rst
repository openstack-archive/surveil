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


