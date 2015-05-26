FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>

RUN apt-get update && apt-get install -y vim python-pip python3-pip python-dev libffi-dev libssl-dev git python-pycurl

# Surveil needs alignak (as a lib)
RUN useradd shinken && pip install https://github.com/Alignak-monitoring/alignak/archive/396d10105827f8c75686811991829548e6778e11.zip

# python-surveilclient (used by surveil-init)
RUN pip install python-surveilclient==0.5.1

# Download packs
ENV MONITORING_TOOLS_VERSION 0.2.0
RUN apt-get install -y subversion && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/generic-host /packs/generic-host && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/linux-glance /packs/linux-glance && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/linux-cinder /packs/linux-cinder && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/linux-keystone /packs/linux-keystone && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/linux-nova /packs/linux-nova && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/packs/linux-openstackceilometer /packs/linux-openstackceilometer && \
    apt-get remove -y subversion

ADD requirements.txt /opt/surveil/requirements.txt
RUN pip install -r /opt/surveil/requirements.txt

ADD tools/docker/surveil_container/setup.sh /opt/surveil/setup.sh
ADD setup.py /opt/surveil/setup.py
ADD setup.cfg /opt/surveil/setup.cfg
ADD README.rst /opt/surveil/README.rst
ADD etc/surveil /etc/surveil
ADD surveil /opt/surveil/surveil

#ADD .git /surveil/.git
ENV PBR_VERSION=PROD

# We are using develop so that the code can be mounted when in DEV.
RUN cd /opt/surveil && python setup.py develop

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
