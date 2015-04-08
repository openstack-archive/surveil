FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>

RUN apt-get update && apt-get install -y vim supervisor python-pip python3-pip python-dev libffi-dev libssl-dev git python-pycurl

# Surveil needs shinken (as a lib)
RUN useradd shinken && pip install https://github.com/naparuba/shinken/archive/2.2-RC1.zip

# python-surveilclient (used by surveil-init)
RUN pip install python-surveilclient

# Download packs
RUN apt-get install -y subversion && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/packs/generic-host /packs/generic-host && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/packs/linux-glance /packs/linux-glance && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/packs/linux-keystone /packs/linux-keystone && \
    apt-get remove -y subversion

ADD requirements.txt surveil/requirements.txt
ADD setup.py /surveil/setup.py
ADD setup.cfg /surveil/setup.cfg
ADD README.rst /surveil/README.rst
ADD .git /surveil/.git
ADD etc/surveil /etc/surveil

# Install
RUN pip install -r /surveil/requirements.txt

# Supervisor
ADD tools/docker/surveil_container/etc/supervisor /etc/supervisor

# Surveil API
EXPOSE 8080

CMD sleep 20 && \
    cd /surveil/ && \
    python setup.py develop && \
    /usr/bin/supervisord
