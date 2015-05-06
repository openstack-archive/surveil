#!/bin/bash


function setup_surveil_api {
    sed -i "s/pipeline =.*/pipeline = ${SURVEIL_AUTH_BACKEND} api-server/" /etc/surveil/api_paste.ini
}

if [ -f "/.surveil_api_setup" ]; then
    echo "=> Surveil API was already configured, skipping..."
else
    echo -e "=> Configuring Surveil API..."
    setup_surveil_api && touch "/.surveil_api_setup"
    echo -e "=> Done with API configuration."
fi
