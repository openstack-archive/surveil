Changelog
#########

0.13.0
~~~~~~

* status API: New metrics enpoints
* status API: Events
* mod-ceilometer: Updated to 0.2.1
* docs: Heat autoscaling examples
* Refactored MongoDB handlers
* surveil-api New default port: 5311 (Breaking Change)

0.12.0
~~~~~~

* surveil-os-interface: Include instance metadata in custom fields

0.11.0
~~~~~~

* surveil-init: New options

0.10.4
~~~~~~

* surveil-init: Don't only load pack sub dir

0.10.3
~~~~~~

* Surveil-init: Fixed pymongo 2.5 compatibility

0.10.2
~~~~~~

* mod-mongo-live-config: Fixed collection names
* Alignak: Changed plugin paths to fix packaging

0.10.1
~~~~~~

* Fixed pack names

0.10.0
~~~~~~

* New --influxdb option for surveil-init
* New --mongo-uri parameter for surveil-pack-upload
* Updated surveil-init paths

0.9.2
~~~~~

* Updated paths in surveil-init

0.9.1
~~~~~

* pack_upload.py: Import Alignak instead of Shinken

0.9.0
~~~~~

* New version of python-influxdb
* Updated surveil-init packs paths

0.8.0
~~~~~

* Many documentation improvements
* Metrics api now includes host name
* Renamed rabbitmq-consumer to surveil-os-interface
* Updated InfluxDB to 0.9.0

0.7.0
~~~~~
* Integrate grafana
* Updated mod-ceilometer
* Metrics API: list metric names

0.6.0
~~~~~

* Rabbitconsumer: New daemon to monitor OpenStack's RabbitMQ and automatically create hosts
* Updated mod_mongo_live_config to 0.3.0
* Now determine nova hosts status with nova state

0.5.0
~~~~~

* Load config from /etc/surveil/surveil.cfg
* Added 'long_output' to status API
* Added 'services' to status host API
* Replaced Shinken by Alignak
* Implemented metrics API
* Released surveil-rabbitMQ-consumer (Automatically monitor OpenStack hosts)

0.4.4
~~~~~

* Alignak -> Shinken

0.4.3
~~~~~

* Fixed CPU load issues with mod-booster-nrpe

0.4.2
~~~~~

* Fxied mod-booster-nrpe issues

0.4.1
~~~~~

* Specify monitoring-tools version

0.4.0
~~~~~

* Live states are now loaded from MongoDB
* Install modules from tarballs (stabilise Surveil images)
* Python 3 support

0.3.3
~~~~~

* Require specific surveilclient version

0.3.2
~~~~~

* Fixed issue with python-surveilclient

0.3.1
~~~~~

* Changed keyserver for kaji

0.3.0
~~~~~

* Added parents to Live host API
* Fixed custom_fields issues
* Added support for Macromodulation objects
* Packs are now uploaded in prod

0.2.3
~~~~~

* policy: admins now match surveil:authenticated

0.2.2
~~~~~

* Fixed keystone authentication env vars

0.2.1
~~~~~

* Fixed typo in authtoken

0.2.0
~~~~~

* Config API: notificationways
* Dropped docker-comopse heritage
* Config API: check modulations
* New container variable: SURVEIL_KEYSTONE_ENDPOINT

0.1.0
~~~~~

* Initial release
