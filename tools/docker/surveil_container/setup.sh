#!/bin/bash

function setup_surveil_api {
    if [ $SURVEIL_AUTH_BACKEND = surveil ] ; then
        echo -e "=> Setting up Surveil API for surveil authentication..."
        sed -i "s/pipeline =.*/pipeline = surveil-auth api-server/" /etc/surveil/api_paste.ini
    else
        echo -e "=> Setting up Surveil API for keystone authentication..."
        sed -i "s|pipeline =.*|pipeline = authtoken api-server|" /etc/surveil/api_paste.ini
        sed -i "s|auth_protocol=.*|auth_protocol=${SURVEIL_KEYSTONE_AUTH_PROTOCOL}|" /etc/surveil/api_paste.ini
        sed -i "s|auth_host=.*|auth_host=${SURVEIL_KEYSTONE_HOST}|" /etc/surveil/api_paste.ini
        sed -i "s|admin_user=.*|admin_user=${SURVEIL_OS_USERNAME}|" /etc/surveil/api_paste.ini
        sed -i "s|admin_password=.*|admin_password=${SURVEIL_OS_PASSWORD}|" /etc/surveil/api_paste.ini
        sed -i "s|admin_tenant_name=.*|admin_tenant_name=${SURVEIL_OS_TENANT_NAME}|" /etc/surveil/api_paste.ini
    fi
}

if [ -f "/.surveil_api_setup" ]; then
    echo "=> Surveil API was already configured, skipping..."
else
    setup_surveil_api && touch "/.surveil_api_setup"
    echo -e "=> Done with API configuration."
fi
