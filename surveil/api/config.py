# Copyright 2014 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from surveil.api import hooks

# Server Specific Configurations
server = {
    'port': 8080,
    'host': '0.0.0.0'
}


# In the future, surveil_api_config could be loaded from somewhere else,
# as long as is it in the same format.
surveil_api_config = {
    "mongodb_uri": "mongodb://mongo:27017",
    "ws_arbiter_url": "http://alignak:7760",
    "influxdb_uri": "influxdb://root:root@influxdb:8086/db"
}

app_hooks = [
    hooks.DBHook(
        surveil_api_config['mongodb_uri'],
        surveil_api_config['ws_arbiter_url'],
        surveil_api_config['influxdb_uri']
    )
]

# Pecan Application Configurations
app = {
    'root': 'surveil.api.controllers.root.RootController',
    'modules': ['surveil.api'],
    'template_path': '%(confdir)s/pecanrest/templates',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    },
    'hooks': app_hooks,
}

logging = {
    'loggers': {
        'root': {'level': 'INFO', 'handlers': ['console']},
        'pecanrest': {'level': 'DEBUG', 'handlers': ['console']},
        'pecan.commands.serve': {'level': 'DEBUG', 'handlers': ['console']},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        },
        'color': {
            '()': 'pecan.log.ColorFormatter',
            'format': ('%(asctime)s [%(padded_color_levelname)s] [%(name)s]'
                       '[%(threadName)s] %(message)s'),
            '__force_dict__': True
        }
    }
}
