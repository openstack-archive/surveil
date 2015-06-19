Installing Surveil
------------------

Surveil is currently packaged for Centos 7. You can install it via our custom repositories.

0. Installing the repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the RDO repositories with the following command: ::

    yum install -y https://rdoproject.org/repos/rdo-release.rpm

Install the Surveil repositories with the following command: ::

    yum install -y yum-utils
    yum-config-manager --add-repo http://yum.surveil.io/centos_7/

1. Installing Surveil
~~~~~~~~~~~~~~~~~~~~~

All-in-One installation: ``survei-full``
****************************************

Surveil does not work with SELinux yet. To disable it, use the following commands: ::

    echo 0 >  /sys/fs/selinux/enforce
    sed -i 's/SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config

Install surveil-full with the following command: ::

    yum install -y surveil-full --nogpgcheck


Due to an issue with MongoDB presenting itself as running before it is ready, start it 20 seconds before the other services: ::

    systemctl start mongod.service

Launch all surveil services with the following command: ::

    systemctl start surveil-full.target


The surveil-init command will create a database in InfluxDB and initialize the MongoDB database: ::

    surveil-init --influxdb

The surveil-webui-init command will pre-create data sources in Grafana: ::

    surveil-webui-init -H localhost -U root -P root -p 8086 -g "http://localhost:3000/grafana"


2. Testing the API
~~~~~~~~~~~~~~~~~~

You should now be able to use the API: ::

    surveil status-host-list
    surveil config-host-list

3. Surveil Web UI
~~~~~~~~~~~~~~~~~

Access the Surveil Web UI at http://localhost:80
