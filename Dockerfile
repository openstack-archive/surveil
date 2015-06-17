FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>

RUN apt-get update && apt-get install -y vim python-pip python3-pip python-dev libffi-dev libssl-dev git python-pycurl python-virtualenv libcurl4-openssl-dev

# VirtualEnv
RUN virtualenv /opt/surveil/env

# Surveil needs alignak (as a lib)
RUN useradd alignak && /opt/surveil/env/bin/pip install pycurl https://github.com/Alignak-monitoring/alignak/archive/d7f457d5ed94f08d9a6a38809106d3e0d35a1712.tar.gz

# Download packs
ENV MONITORING_TOOLS_VERSION 0.4.0
RUN apt-get install -y subversion && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/generic-host /usr/share/monitoring/packs/sfl/generic-host && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/openstack-glance-http /usr/share/monitoring/packs/sfl/openstack-glance-http && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/openstack-cinder-http /usr/share/monitoring/packs/sfl/openstack-cinder-http && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/openstack-keystone-http /usr/share/monitoring/packs/sfl/openstack-keystone-http && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/openstack-nova-http /usr/share/monitoring/packs/sfl/openstack-nova-http && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/openstack-host /usr/share/monitoring/packs/openstack-host && \
    apt-get remove -y subversion

ADD requirements.txt /opt/surveil/requirements.txt
RUN /opt/surveil/env/bin/pip install -U "pbr>=0.6,!=0.7,<1.0"
RUN /opt/surveil/env/bin/pip install -r /opt/surveil/requirements.txt

ADD tools/docker/surveil_container/setup.sh /opt/surveil/setup.sh
ADD setup.py /opt/surveil/setup.py
ADD setup.cfg /opt/surveil/setup.cfg
ADD README.rst /opt/surveil/README.rst
ADD etc/surveil /etc/surveil
ADD surveil /opt/surveil/surveil

#ADD .git /surveil/.git
ENV PBR_VERSION=PROD

# We are using develop so that the code can be mounted when in DEV.
RUN cd /opt/surveil && /opt/surveil/env/bin/python setup.py develop
ENV PATH=$PATH:/opt/surveil/env/bin

# Set to 'surveil' or 'keystone'
ENV SURVEIL_AUTH_BACKEND=surveil
ENV SURVEIL_KEYSTONE_HOST=198.72.123.131
ENV SURVEIL_KEYSTONE_AUTH_PROTOCOL=http

# OpenStack Authentication credentials. Used for Keystone authentication
ENV SURVEIL_OS_USERNAME=admin
ENV SURVEIL_OS_PASSWORD=password
ENV SURVEIL_OS_TENANT_NAME=admin

CMD cd /opt/surveil && \
    ./setup.sh && \
    ((sleep 40 && surveil-init) &) && \
    surveil-api
