FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>

RUN apt-get update && apt-get install -y vim python-pip python3-pip python-dev libffi-dev libssl-dev git python-pycurl

# Surveil needs shinken (as a lib)
RUN useradd shinken && pip install https://github.com/naparuba/shinken/archive/2.2-RC1.zip

# python-surveilclient (used by surveil-init)
RUN pip install "python-surveilclient>=0.4.1"

# Download packs
RUN apt-get install -y subversion && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/packs/generic-host /packs/generic-host && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/packs/linux-glance /packs/linux-glance && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/packs/linux-keystone /packs/linux-keystone && \
    apt-get remove -y subversion

ADD requirements.txt surveil/requirements.txt
RUN pip install -r /surveil/requirements.txt

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

#Set to 'surveil' or 'keystone'
ENV SURVEIL_AUTH_BACKEND=surveil
ENV SURVEIL_KEYSTONE_ENDPOINT=127.0.0.1

CMD cd /opt/surveil && \
    ./setup.sh && \
    surveil-api
