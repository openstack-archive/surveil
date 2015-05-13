FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>

RUN apt-get update && apt-get install -y vim supervisor python-dev libffi-dev libssl-dev nagios-nrpe-server
# libffi-devand libssl-dev are for python-cryptography

### Shinken
RUN apt-get update && apt-get install -y python-pip git
RUN useradd shinken && pip install https://github.com/gst/shinken/archive/19df05f2da13bdc6957ef1adf0660aa9f61c89f7.zip
RUN apt-get install -y python-pycurl
RUN shinken --init

## modules
RUN shinken install webui
RUN shinken install auth-cfg-password
RUN shinken install booster-nrpe
RUN pip install influxdb==2.3.0 && shinken install mod-influxdb
RUN shinken install ws-arbiter
RUN pip install pymongo==2.8 && shinken install mod-mongodb

RUN cd /opt && \
    git clone  https://github.com/savoirfairelinux/mod-mongo-live-config.git && \
    cd mod-mongo-live-config && \
    git checkout 39e43d9a1a2f80c7db6db085ed0df388dc1fef23 && \
    git reset --hard && \
    cd /var/lib/shinken/modules && \
    ln -s /opt/mod-mongo-live-config/src/mod_mongo_live_config

## plugins
RUN apt-get update && apt-get install -y nagios-plugins nagios-nrpe-plugin
# run permissions for user `shinken`
RUN chmod u+s /usr/lib/nagios/plugins/check_icmp
RUN chmod u+s /bin/ping
RUN chmod u+s /bin/ping6

# Download plugins
RUN apt-get update && apt-get install -y subversion && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/plugins/check-glance /plugins/check_glance && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/plugins/check-keystone /plugins/check_keystone && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/plugins/check-nova /plugins/check_nova && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/trunk/plugins/check-cinder /plugins/check_cinder && \
    apt-get remove -y subversion

## Install plugins dependencies
RUN pip install shinkenplugins python-keystoneclient python-glanceclient

## Install Plugins
RUN cd /plugins/check_glance && sudo python setup.py install
RUN cd /plugins/check_keystone && sudo python setup.py install
RUN cd /plugins/check_nova && sudo python setup.py install
RUN cd /plugins/check_cinder && sudo python setup.py install

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
