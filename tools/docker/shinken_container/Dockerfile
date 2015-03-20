FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>


RUN apt-get update
RUN apt-get install -y vim supervisor python-dev libffi-dev libssl-dev
# libffi-devand libssl-dev are for python-cryptography

### Shinken
RUN apt-get install -y python-pip
RUN sh  -c 'gpg --recv-keys --keyserver pgp.mit.edu 2320E8F8 && gpg --export --armor 2320E8F8 | apt-key add -' && \
    echo 'deb http://deb.kaji-project.org/ubuntu14.04/ amakuni main' >> /etc/apt/sources.list.d/kaji.list && \
    apt-get update
RUN apt-get install -y shinken-common
# RUN useradd shinken && export PBR_VERSION=useless && pip install --install-option="--prefix=/" https://github.com/naparuba/shinken/archive/2.4-BETA1.zip
RUN shinken --init

## modules
RUN mkdir /var/lib/shinken/share /var/lib/shinken/doc /var/lib/shinken/inventory
RUN shinken install webui
RUN shinken install auth-cfg-password
RUN pip install https://github.com/influxdb/influxdb-python/archive/0.9.0_support.zip && shinken install mod-influxdb
RUN shinken install ws-arbiter
RUN pip install pymongo && shinken install mod-mongodb

## plugins
RUN apt-get install -y nagios-plugins
# run permissions for user `shinken`
RUN chmod u+s /usr/lib/nagios/plugins/check_icmp
RUN chmod u+s /bin/ping
RUN chmod u+s /bin/ping6

# Download plugins
RUN apt-get install -y subversion && \
    svn checkout https://github.com/stackforge/surveil/trunk/shinken-tools/plugins/plugin-check-glance /plugins/check_glance && \
    svn checkout https://github.com/stackforge/surveil/trunk/shinken-tools/plugins/plugin-check-keystone /plugins/check_keystone && \
    apt-get remove -y subversion

## Install plugins dependencies
RUN pip install shinkenplugins python-keystoneclient python-glanceclient

## Install Plugins
RUN mkdir -p /usr/lib/shinken/plugins && \
    cp /plugins/*/check_* /usr/lib/shinken/plugins/

## configuration
RUN rm -rf /etc/shinken
ADD etc/shinken /etc/shinken
RUN chown -R root:shinken /etc/shinken

### Supervisor
ADD etc/supervisor /etc/supervisor

# Shinken WEBUI
EXPOSE 7767

# ws-arbiter
EXPOSE 7760

CMD /usr/bin/supervisord
