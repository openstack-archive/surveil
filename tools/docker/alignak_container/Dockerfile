FROM ubuntu:trusty

MAINTAINER Alexandre Viau <alexandre.viau@savoirfairelinux.com>

RUN apt-get update && apt-get install -y vim git supervisor python-dev libffi-dev libssl-dev nagios-nrpe-server wget python-virtualenv python-openssl
# libffi-devand libssl-dev are for python-cryptography

### Alignak
RUN apt-get update && apt-get install -y python-pip python-pycurl
RUN useradd alignak && pip install https://github.com/Alignak-monitoring/alignak/archive/d7f457d5ed94f08d9a6a38809106d3e0d35a1712.tar.gz

## modules
# mod-webui
RUN cd /tmp && \
    wget -O mod-webui.tar.gz https://github.com/shinken-monitoring/mod-webui/archive/3215d6c775326d1fb3afb161eb279dfb44e45986.tar.gz && \
    tar -zxvf mod-webui.tar.gz && \
    mv /tmp/mod-webui-*/module /var/lib/alignak/modules/webui && \
    rm -rfv /tmp/mod-webui*

# auth-cfg-password
RUN cd /tmp && \
    wget -O mod-auth-cfg-password.tar.gz https://github.com/shinken-monitoring/mod-auth-cfg-password/archive/6079d31974305b74e332424df44efecc9dfeabfc.tar.gz && \
    tar -zxvf mod-auth-cfg-password.tar.gz && \
    mv /tmp/mod-auth-cfg-password-*/module /var/lib/alignak/modules/auth-cfg-password && \
    rm -rfv /tmp/mod-auth-cfg-password*

# mod-booster-nrpe
RUN cd /tmp && \
    wget -O mod-booster-nrpe.tar.gz https://github.com/shinken-monitoring/mod-booster-nrpe/archive/de7099706855e32c1962c77740be0fae446d15f5.tar.gz && \
    tar -zxvf mod-booster-nrpe.tar.gz && \
    mv /tmp/mod-booster-nrpe-*/module /var/lib/alignak/modules/mod-booster-nrpe && \
    rm -rfv /tmp/mod-booster-nrpe*

# mod-surveil
RUN pip install python-surveilclient==0.13.3
RUN cd /tmp && \
    wget -O mod-surveil-config.tar.gz https://github.com/Alignak-monitoring/mod-surveil/archive/fdc98b4fc036aa483ecb58459f11f9a87cf2254a.tar.gz && \
    tar -zxvf mod-surveil-config.tar.gz && \
    mv /tmp/mod-surveil-*/alignak/modules/mod_surveil /var/lib/alignak/modules/mod-surveil && \
    rm -rfv /tmp/mod-surveil*

# mod-influxdb
RUN pip install influxdb==2.8.0
RUN cd /tmp && \
    wget -O mod-influxdb.tar.gz https://github.com/savoirfairelinux/mod-influxdb/archive/9433b726492a09d5faeb70abfc5efdbf1728686f.tar.gz && \
    tar -zxvf mod-influxdb.tar.gz && \
    mv /tmp/mod-influxdb-*/module /var/lib/alignak/modules/mod-influxdb && \
    rm -rfv /tmp/mod-influxdb*

# mod-ws-arbiter
RUN cd /tmp && \
    wget -O mod-ws-arbiter.tar.gz https://github.com/shinken-monitoring/mod-ws-arbiter/archive/ebae7950be9452ab80ec58575e9887d9b2a15d2a.tar.gz && \
    tar -zxvf mod-ws-arbiter.tar.gz && \
    mv /tmp/mod-ws-arbiter-*/module /var/lib/alignak/modules/ws-arbiter && \
    rm -rfv /tmp/mod-ws-arbiter*

# mod-mongo-live-config
RUN pip install pymongo==3.0.2
RUN cd /tmp && \
    wget -O mod-mongo-live-config.tar.gz https://github.com/savoirfairelinux/mod-mongo-live-config/archive/0.3.2.tar.gz && \
    tar -zxvf mod-mongo-live-config.tar.gz && \
    mv /tmp/mod-mongo-live-config-*/mod_mongo_live_config /var/lib/alignak/modules/mod_mongo_live_config && \
    rm -rfv /tmp/mod-mongo-live-config*

# mod-ceilometer
RUN apt-get update && apt-get install -y python-ceilometerclient
RUN cd /tmp && \
    wget -O mod-ceilometer.tar.gz https://github.com/savoirfairelinux/mod-ceilometer/archive/0.2.1.tar.gz && \
    tar -zxvf mod-ceilometer.tar.gz && \
    mv /tmp/mod-ceilometer-*/module /var/lib/alignak/modules/mod-ceilometer && \
    rm -rfv /tmp/mod-ceilometer*

## plugins
RUN apt-get update && apt-get install -y nagios-plugins nagios-nrpe-plugin
# run permissions for user `alignak`
RUN chmod u+s /usr/lib/nagios/plugins/check_icmp
RUN chmod u+s /bin/ping
RUN chmod u+s /bin/ping6

# Download plugins
ENV MONITORING_TOOLS_VERSION 0.4.1
RUN apt-get update && apt-get install -y subversion && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-glance /plugins/check_glance && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-keystone /plugins/check_keystone && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-nova /plugins/check_nova && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-cinder /plugins/check_cinder && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-ceilometer /plugins/check_ceilometer && \
    svn checkout https://github.com/savoirfairelinux/monitoring-tools/tags/${MONITORING_TOOLS_VERSION}/plugins/check-nova-host-status /plugins/check_nova_host_status && \
    apt-get remove -y subversion

## Install plugins dependencies
RUN mkdir -p /opt/surveilplugins
RUN virtualenv /opt/surveilplugins/env
ENV PATH=$PATH:/opt/surveilplugins/env/bin
RUN /opt/surveilplugins/env/bin/pip install -U "pbr>=1.3,<2.0" shinkenplugins python-keystoneclient python-glanceclient

## Install Plugins
RUN mkdir -p /usr/lib/monitoring/plugins/sfl
RUN cd /plugins/check_keystone && sudo /opt/surveilplugins/env/bin/python setup.py install && ln -s /opt/surveilplugins/env/bin/check_keystone /usr/lib/monitoring/plugins/sfl/
RUN cd /plugins/check_glance && sudo /opt/surveilplugins/env/bin/python setup.py install && ln -s /opt/surveilplugins/env/bin/check_glance  /usr/lib/monitoring/plugins/sfl/
RUN cd /plugins/check_nova && sudo /opt/surveilplugins/env/bin/python setup.py install && ln -s /opt/surveilplugins/env/bin/check_nova /usr/lib/monitoring/plugins/sfl/
RUN cd /plugins/check_cinder && sudo /opt/surveilplugins/env/bin/python setup.py install && ln -s /opt/surveilplugins/env/bin/check_cinder /usr/lib/monitoring/plugins/sfl/
RUN cd /plugins/check_ceilometer && sudo /opt/surveilplugins/env/bin/python setup.py install && ln -s /opt/surveilplugins/env/bin/check_ceilometer /usr/lib/monitoring/plugins/sfl/
RUN cd /plugins/check_nova_host_status && sudo /opt/surveilplugins/env/bin/python setup.py install && ln -s /opt/surveilplugins/env/bin/check_nova_host_status /usr/lib/monitoring/plugins/sfl/

## Add check example plugin
ADD plugins/check-example /plugins/check_example
RUN virtualenv /plugins/check_example/env
ENV PATH=$PATH:/plugins/check_example/env/bin
RUN /plugins/check_example/env/bin/pip install -r /plugins/check_example/requirements.txt
RUN cd /plugins/check_example && sudo /opt/surveilplugins/env/bin/python setup.py install && ln -s /opt/surveilplugins/env/bin/check_example /usr/lib/monitoring/plugins/sfl

## configuration
ADD setup.sh /setup.sh
RUN rm -rf /etc/alignak
ADD etc/alignak /etc/alignak

RUN chown -R root:alignak /etc/alignak

### Supervisor
ADD etc/supervisor /etc/supervisor

# Alignak WEBUI
EXPOSE 7767

# ws-arbiter
EXPOSE 7760

# OpenStack Authentication credentials. Used for sending data to Ceilometer
ENV SURVEIL_OS_AUTH_URL=http://keystone:5000/v2.0
ENV SURVEIL_OS_USERNAME=admin
ENV SURVEIL_OS_PASSWORD=password
ENV SURVEIL_OS_TENANT_NAME=admin

CMD ./setup.sh && /usr/bin/supervisord
