FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>


RUN apt-get update
RUN apt-get install -y vim

### Shinken
RUN apt-get install -y python-pip
RUN useradd shinken && pip install https://github.com/naparuba/shinken/archive/master.tar.gz
RUN apt-get install -y python-pycurl
RUN shinken --init

## modules
#RUN mkdir /var/lib/shinken/share
RUN shinken install webui
RUN shinken install auth-cfg-password
RUN pip install influxdb && shinken install mod-influxdb
RUN shinken install ws-arbiter
RUN pip install pymongo && shinken install mod-mongodb

## plugins
RUN apt-get install -y nagios-plugins
# run permissions for user `shinken`
RUN chmod u+s /usr/lib/nagios/plugins/check_icmp
RUN chmod u+s /bin/ping
RUN chmod u+s /bin/ping6

## Packs
ADD shinken-tools/packs /packs

## Plugins
ADD shinken-tools/plugins/*/check_* /usr/lib/nagios/plugins/

# Download packs from savoirfairelinux/monitoring-tools
RUN apt-get install -y subversion && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/packs/generic-host /packs/generic-host && \
    apt-get remove -y subversion

## configuration
RUN rm -rf /etc/shinken
ADD tools/docker/etc/shinken /etc/shinken
RUN chown -R root:shinken /etc/shinken

### Surveil
## Copy files
ADD surveil /surveil/surveil
ADD setup.cfg /surveil/setup.cfg
ADD requirements.txt surveil/requirements.txt
ADD setup.py /surveil/setup.py
ADD .git /surveil/.git
ADD README.rst surveil/README.rst

## Install
RUN apt-get install -y python3-pip python-dev libffi-dev libssl-dev
RUN pip install -r /surveil/requirements.txt
RUN apt-get install -y git
RUN cd surveil && python setup.py install

### Supervisor
RUN apt-get -y install supervisor
ADD tools/docker/etc/supervisor /etc/supervisor

# Shinken WEBUI
EXPOSE 7767

# Surveil
EXPOSE 8080

CMD surveil-init && \
    surveil-pack-upload --mongo-url=mongo --mongo-port=27017 /packs/linux-keystone/ && \
    surveil-pack-upload --mongo-url=mongo --mongo-port=27017 /packs/linux-glance/ && \
    surveil-pack-upload --mongo-url=mongo --mongo-port=27017 /packs/generic-host/ && \
    /usr/bin/supervisord
