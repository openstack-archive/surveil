Installing Surveil
------------------

Surveil is currently packaged for Centos 7. You can install it via our custom repositories.

0. Installing the repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the RDO repositories with the following command: ::

    yum install -y https://rdoproject.org/repos/rdo-release.rpm

Install the Surveil repositories with the following command: ::

    yum install -y yum-utils
    yum-config-manager --add-repo http://yum.surveil.savoirfairelinux.net/centos_7/

1. Installing Surveil
~~~~~~~~~~~~~~~~~~~~~

All-in-One installation: ``survei-full``
****************************************

Install surveil-full with the following command: ::

    yum install -y surveil-full

Launch all surveil services with the following command: ::

    systemctl start surveil-full.target


2. Testing the API
~~~~~~~~~~~~~~~~~~

You should now be able to use the API: ::

    export SURVEIL_API_URL=http://localhost:8080/v2
    export SURVEIL_AUTH_URL=http://localhost:8080/v2/auth
    surveil status-host-list
    surveil config-host-list

