FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>

RUN apt-get update && apt-get install -y vim supervisor python-dev libffi-dev libssl-dev nagios-nrpe-server
# libffi-devand libssl-dev are for python-cryptography

### Shinken
RUN apt-get update && apt-get install -y python-pip
RUN useradd shinken && pip install https://github.com/naparuba/shinken/archive/2.4-RC3.zip
RUN apt-get install -y python-pycurl
RUN shinken --init

## modules
RUN shinken install webui
RUN shinken install auth-cfg-password
RUN shinken install booster-nrpe
RUN pip install influxdb && shinken install mod-influxdb
RUN shinken install ws-arbiter
RUN pip install pymongo==2.8 && shinken install mod-mongodb

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
    apt-get remove -y subversion

## Install plugins dependencies
RUN pip install shinkenplugins python-keystoneclient python-glanceclient

## Install Plugins
RUN cd /plugins/check_glance && sudo pip install --upgrade .
RUN cd /plugins/check_keystone && sudo pip install --upgrade .
RUN cd /plugins/check_nova && sudo pip install --upgrade .

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
