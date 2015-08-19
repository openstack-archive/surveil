Components of a container
~~~~~~~~~~~~~~~~~~~~~~~~~

info
****
Show all information pf a Surveil objects
::

  {
      "type": "info",
      "attributes": {
          "inputSource": {
              "MyTileTitle": "myInputSource"
      }
  }

MyTileTitle (required)
    Tile of the tile
myInputSource
    key of the var fillParams inside container.js file .This key select the type of object in the tile

host main
*********
Show inside a tile the address and the alias of a host
::

  {
      "type": "host-main",
      "attributes": {}
  }

host live
*********
Show inside a tile the host state, its output and it's state icon
::

  {
      "type": "host-live",
      "attributes": {}
  }

host load
*********
Show inside a tile the load metrics state, its output and it's state icon for an host
::

  {
      "type": "host-load",
      "attributes": {}
  }

host cpu
********
Show inside a tile the cpu metrics state, its output and it's state icon for an host
::

  {
      "type": "host-cpu",
      "attributes": {}
  }

host service list
*****************
Show inside a tile the service description, its acknowledge and its status for all service hosts
::

  {
      "type": "host-services-list",
      "attributes": {}
  }

service main
************
Show inside a tile the host attached to a service
::

  {
      "type": "service-main",
      "attributes": {}
  }
service live
************
Show inside a tile the service state, its output and it's state icon
::

  {
      "type": "service-live",
      "attributes": {}
  }

service info
************
Show inside a tile the service description, its acknowledge and its status
::

  {
      "type": "service-info",
      "attributes": {}
  }

service graphs
**************
Show a grafana graph for each service metric
::

  {
      "type": "service-graphs",
      "attributes": {}
  }
