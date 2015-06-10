Monitoring a host with passive checks
-------------------------------------

Surveil allows for both passive monitoring and polling. In this guide, we will be creating a host and send passive check results.


0. Creating the host and service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the Surveil CLI: ::

    surveil config-host-create --host_name passive_check_host --address 127.0.0.1
    surveil config-service-create --host_name passive_check_host --service_description passive_check_service --passive_checks_enabled 1 --check_command _echo --max_check_attempts 4 --check_interval 5 --retry_interval 3 --check_period "24x7" --notification_interval 30 --notification_period "24x7" --contacts admin --contact_groups admins
    surveil config-reload

1. Sending check results
~~~~~~~~~~~~~~~~~~~~~~~~

With the Surveil CLI: ::

    surveil status-submit-check-result --host_name passive_check_host --service_description passive_check_service --output "Hello!" --return_code 0


2. Consulting the status of your host
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the Surveil CLI: ::

    surveil status-service-list

