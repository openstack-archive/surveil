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
RUN mkdir /var/lib/shinken/share
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

## configuration
RUN rm -rf /etc/shinken
ADD tools/docker/etc/shinken /etc/shinken
RUN chown -R root:shinken /etc/shinken

### Influxdb
RUN apt-get install -y wget curl
RUN wget http://s3.amazonaws.com/influxdb/influxdb_latest_amd64.deb
RUN useradd influxdb # We should remove this when issue is fixed (https://github.com/influxdb/influxdb/issues/670)
RUN dpkg -i influxdb_latest_amd64.deb
RUN service influxdb start && until curl -X POST 'http://localhost:8086/db?u=root&p=root' -d '{"name": "grafana"}'; do echo "Try again"; sleep 2; done &&  curl -X POST 'http://localhost:8086/db?u=root&p=root' -d '{"name": "db"}' # We should remove the sleep when this issue is fixed: https://github.com/influxdb/influxdb/issues/805

### Grafana
RUN apt-get install -y apache2
RUN wget http://grafanarel.s3.amazonaws.com/grafana-1.7.0-rc1.tar.gz
RUN tar xvf grafana-1.7.0-rc1.tar.gz
RUN mv grafana-1.7.0-rc1 /var/www/html/grafana
ADD tools/docker/etc/apache2/sites-available/grafana.conf /etc/apache2/sites-available/grafana.conf
ADD tools/docker/var/www/html/grafana/config.js /var/www/html/grafana/config.js

## Influxdb reverse proxy for grafana
RUN apt-get install -y libapache2-mod-proxy-html
RUN a2enmod proxy_http
ADD tools/docker/etc/apache2/conf-enabled/influxdb.conf /etc/apache2/conf-enabled/influxdb.conf

### Mongodb
#RUN apt-get install -y mongodb
#ADD tools/docker/etc/mongodb.conf /etc/mongodb.conf

## Import sample config
## TODO: Use the python client or curl instead.
# ADD tools/docker/mongoimport /mongoimport
# RUN service mongodb start && until mongoimport --db shinken --host localhost --collection hosts < /mongoimport/hosts.json; do echo "Try again"; sleep 2; done && mongoimport --db shinken --host localhost --collection services < /mongoimport/services.json

### Surveil
## Copy files
ADD surveil /surveil/surveil
ADD setup.cfg /surveil/setup.cfg
ADD requirements.txt surveil/requirements.txt
ADD setup.py /surveil/setup.py
ADD .git /surveil/.git
ADD README.rst surveil/README.rst

## Install
RUN apt-get install -y python3-pip
RUN pip3 install -r /surveil/requirements.txt
RUN apt-get install -y git
RUN cd surveil && python3 setup.py install

### Supervisor
RUN apt-get -y install supervisor
ADD tools/docker/etc/supervisor /etc/supervisor

# Shinken WEBUI
EXPOSE 7767

# Influxdb
EXPOSE 8083
EXPOSE 8084
EXPOSE 8086

# Grafana
EXPOSE 80

# Mongodb
EXPOSE 27017

# Surveil
EXPOSE 8080

CMD surveil-init && /usr/bin/supervisord
