Surveil Web UI
~~~~~~~~~~~~~~

The Surveil Web UI is a web interface for Surveil.

==================================   ==========================
**package name (RPM)**               surveil-webui
**required services**                httpd.service
**Default port**                     80
**configuration (global)**           /etc/surveil-webui/config.json
**configuration (user config)**      /etc/surveil-webui/default_user_config.json
==================================   ==========================

surveil-webui implements the Surveil API. It needs access to the Surveil API endpoint and Grafana. By default, it is packaged with a reverse proxy in ``/etc/http/conf.d/surveil``: ::

    ProxyPass /surveil/surveil/v2/auth/ http://localhost:5311/v2/auth/
    ProxyPassReverse /surveil/v2/auth/ http://localhost:5311/v2/auth/

    ProxyPass /surveil/surveil/ http://localhost:5311/
    ProxyPassReverse /surveil/surveil/ http://localhost:5311/

    RequestHeader set GRAFANA-USER "admin"
    ProxyPass /surveil/grafana/ http://localhost:3000/
    ProxyPassReverse /surveil/grafana/ http://localhost:3000/

