#!/bin/bash

function setup_alignak {
    echo -e "Setting up mod-ceilometer"
    sed -i "s|<- SURVEIL_OS_AUTH_URL ->|${SURVEIL_OS_AUTH_URL}|" /etc/alignak/modules/ceilometer.cfg
    sed -i "s|<- SURVEIL_OS_USERNAME ->|${SURVEIL_OS_USERNAME}|" /etc/alignak/modules/ceilometer.cfg
    sed -i "s|<- SURVEIL_OS_PASSWORD ->|${SURVEIL_OS_PASSWORD}|" /etc/alignak/modules/ceilometer.cfg
    sed -i "s|<- SURVEIL_OS_TENANT_NAME ->|${SURVEIL_OS_TENANT_NAME}|" /etc/alignak/modules/ceilometer.cfg
}

if [ -f "/.setup_alignak" ]; then
    echo "=> Alignak was already configured, skipping..."
else
    setup_alignak && touch "/.setup_alignak"
    echo -e "=> Done with Alignak configuration."
fi
