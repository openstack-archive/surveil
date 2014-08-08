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
RUN shinken install webui
RUN shinken install auth-cfg-password
RUN pip install influxdb && shinken install mod-influxdb
RUN shinken install ws-arbiter

## plugins
RUN apt-get install -y nagios-plugins
# run permissions for user `shinken`
RUN chmod u+s /usr/lib/nagios/plugins/check_icmp
RUN chmod u+s /bin/ping
RUN chmod u+s /bin/ping6

## configuration
RUN rm -rf /etc/shinken
ADD etc/shinken /etc/shinken
RUN chown -R root:shinken /etc/shinken

### Influxdb
RUN apt-get install -y wget curl
RUN wget http://s3.amazonaws.com/influxdb/influxdb_latest_amd64.deb
RUN useradd influxdb # We should remove this when issue is fixed (https://github.com/influxdb/influxdb/issues/670)
RUN dpkg -i influxdb_latest_amd64.deb
RUN service influxdb start && sleep 10 && curl -X POST 'http://localhost:8086/db?u=root&p=root' -d '{"name": "grafana"}' &&  curl -X POST 'http://localhost:8086/db?u=root&p=root' -d '{"name": "db"}' # We should remove the sleep when this issue is fixed: https://github.com/influxdb/influxdb/issues/805

### Riemann
RUN wget http://aphyr.com/riemann/riemann_0.2.6_all.deb
RUN sudo dpkg -i riemann_0.2.6_all.deb
RUN sudo apt-get install -y openjdk-7-jre
ADD etc/riemann/riemann.config /etc/riemann/riemann.config

### Grafana
RUN apt-get install -y apache2
RUN wget http://grafanarel.s3.amazonaws.com/grafana-1.7.0-rc1.tar.gz
RUN tar xvf grafana-1.7.0-rc1.tar.gz
RUN mv grafana-1.7.0-rc1 /var/www/html/grafana
ADD etc/apache2/sites-available/grafana.conf /etc/apache2/sites-available/grafana.conf
ADD var/www/html/grafana/config.js /var/www/html/grafana/config.js

## Influxdb reverse proxy for grafana
RUN apt-get install -y libapache2-mod-proxy-html
RUN a2enmod proxy_http
ADD etc/apache2/conf-enabled/influxdb.conf /etc/apache2/conf-enabled/influxdb.conf

### Supervisor
RUN apt-get -y install supervisor
ADD etc/supervisor /etc/supervisor

# Shinken WEBUI
EXPOSE 7767 

# Influxdb
EXPOSE 8083
EXPOSE 8084
EXPOSE 8086

# Grafana
EXPOSE 80

# Riemann
EXPOSE 5555

CMD ["/usr/bin/supervisord"]
