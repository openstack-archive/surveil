FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>

RUN apt-get update && apt-get install -y vim supervisor python-dev libffi-dev libssl-dev nagios-nrpe-server wget
# libffi-devand libssl-dev are for python-cryptography

### Alignak
RUN apt-get update && apt-get install -y python-pip git
RUN useradd shinken && pip install https://github.com/naparuba/shinken/archive/601a9cd74ddbc2082f44a8275788d965b700ab3f.zip
RUN apt-get install -y python-pycurl
RUN shinken --init

## modules
RUN shinken install webui
RUN shinken install auth-cfg-password

# mod-booster-nrpe
RUN cd /tmp && \
    wget -O mod-booster-nrpe.tar.gz https://github.com/shinken-monitoring/mod-booster-nrpe/archive/de7099706855e32c1962c77740be0fae446d15f5.tar.gz && \
    tar -zxvf mod-booster-nrpe.tar.gz && \
    mv /tmp/mod-booster-nrpe-*/module /var/lib/shinken/modules/mod-booster-nrpe && \
    rm -rfv /tmp/mod-booster-nrpe*

# mod-mongodb
RUN pip install pymongo==3.0.2
RUN cd /tmp && \
    wget -O mod-mongodb.tar.gz https://github.com/shinken-monitoring/mod-mongodb/archive/5396fded1c56d57202236d1236703a160aec7375.tar.gz && \
    tar -zxvf mod-mongodb.tar.gz && \
    mv /tmp/mod-mongodb-*/module /var/lib/shinken/modules/mod-mongodb && \
    rm -rfv /tmp/mod-mongodb*

# mod-influxdb
RUN pip install influxdb==2.3.0
RUN cd /tmp && \
    wget -O mod-influxdb.tar.gz https://github.com/savoirfairelinux/mod-influxdb/archive/28c1bf1a34748002ad8ee1404123579373ce82fd.tar.gz && \
    tar -zxvf mod-influxdb.tar.gz && \
    mv /tmp/mod-influxdb-*/module /var/lib/shinken/modules/mod-influxdb && \
    rm -rfv /tmp/mod-influxdb*

# mod-ws-arbiter
RUN cd /tmp && \
    wget -O mod-ws-arbiter.tar.gz https://github.com/shinken-monitoring/mod-ws-arbiter/archive/ebae7950be9452ab80ec58575e9887d9b2a15d2a.tar.gz && \
    tar -zxvf mod-ws-arbiter.tar.gz && \
    mv /tmp/mod-ws-arbiter-*/module /var/lib/shinken/modules/ws-arbiter && \
    rm -rfv /tmp/mod-ws-arbiter*

# mod-mongo-live-config
RUN cd /tmp && \
    wget -O mod-mongo-live-config.tar.gz https://github.com/savoirfairelinux/mod-mongo-live-config/archive/0.2.0.tar.gz && \
    tar -zxvf mod-mongo-live-config.tar.gz && \
    mv /tmp/mod-mongo-live-config-*/mod_mongo_live_config /var/lib/shinken/modules/mod_mongo_live_config && \
    rm -rfv /tmp/mod-mongo-live-config*

## plugins
RUN apt-get update && apt-get install -y nagios-plugins nagios-nrpe-plugin
# run permissions for user `shinken`
RUN chmod u+s /usr/lib/nagios/plugins/check_icmp
RUN chmod u+s /bin/ping
RUN chmod u+s /bin/ping6

# Download plugins
ENV MONITORING_TOOLS_VERSION 0.2.0
RUN apt-get update && apt-get install -y subversion && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-glance /plugins/check_glance && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-keystone /plugins/check_keystone && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-nova /plugins/check_nova && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-cinder /plugins/check_cinder && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-ceilometer /plugins/check_ceilometer && \
    apt-get remove -y subversion

## Install plugins dependencies
RUN pip install shinkenplugins python-keystoneclient python-glanceclient

## Install Plugins
RUN cd /plugins/check_glance && sudo python setup.py install
RUN cd /plugins/check_keystone && sudo python setup.py install
RUN cd /plugins/check_nova && sudo python setup.py install
RUN cd /plugins/check_cinder && sudo python setup.py install
RUN cd /plugins/check_ceilometer && sudo python setup.py install

## packs
RUN sh  -c 'gpg --recv-keys --keyserver keyserver.ubuntu.com 2320E8F8 && gpg --export --armor 2320E8F8 | apt-key add -' && \
    sh -c "echo 'deb http://deb.kaji-project.org/ubuntu14.04/ plugins main' >> /etc/apt/sources.list.d/kaji.list" && \
    apt-get update && \
    apt-get install -y --force-yes monitoring-packs-sfl-generic-host monitoring-packs-sfl-linux-system-nrpe

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
