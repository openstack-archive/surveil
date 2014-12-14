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

### Grafana
RUN apt-get install -y apache2 wget
RUN wget http://grafanarel.s3.amazonaws.com/grafana-1.7.0-rc1.tar.gz
RUN tar xvf grafana-1.7.0-rc1.tar.gz
RUN mv grafana-1.7.0-rc1 /var/www/html/grafana
ADD tools/docker/etc/apache2/sites-available/grafana.conf /etc/apache2/sites-available/grafana.conf
ADD tools/docker/var/www/html/grafana/config.js /var/www/html/grafana/config.js

## Influxdb reverse proxy for grafana
RUN apt-get install -y libapache2-mod-proxy-html
RUN a2enmod proxy_http
ADD tools/docker/etc/apache2/conf-enabled/influxdb.conf /etc/apache2/conf-enabled/influxdb.conf

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

# Grafana
EXPOSE 80

# Surveil
EXPOSE 8080

CMD surveil-init && /usr/bin/supervisord
