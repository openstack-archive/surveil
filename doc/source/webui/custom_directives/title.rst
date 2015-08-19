Title
*****

Title writes a header.

.. code-block:: javascript

    {
        "type": "title",
        "attributes": {
            "title": "My big title",
            "item": "host",
            "provider": "nbHostProblems"
        }
    }

title (required)
    the title to write.

item
    A string to print inside the orange banner representing the type of items that is counted by the provider.

provider
    A provider returning a number to write inside the banner. See providers for key.

