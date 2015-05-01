# Copyright 2010-2012 OpenStack Foundation
# Copyright 2015 - Savoir-Faire Linux inc.
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


from surveil.api.authmiddleware import utils

import six

"""
Keystone-Compatible Token-based Authentication Middleware.

This Middleware is based on keystonemiddleware, it creates the same headers but
verifies token authenticity against some other service. It was created for
Surveil so that we can have more flexibility on the authentication backend.

"""


_HEADER_TEMPLATE = {
    'X%s-Domain-Id': 'domain_id',
    'X%s-Domain-Name': 'domain_name',
    'X%s-Project-Id': 'project_id',
    'X%s-Project-Name': 'project_name',
    'X%s-Project-Domain-Id': 'project_domain_id',
    'X%s-Project-Domain-Name': 'project_domain_name',
    'X%s-User-Id': 'user_id',
    'X%s-User-Name': 'username',
    'X%s-User-Domain-Id': 'user_domain_id',
    'X%s-User-Domain-Name': 'user_domain_name',
}


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    def auth_filter(app):
        return AuthProtocol(app, conf)
    return auth_filter


class AuthProtocol(object):
    """Middleware that handles authenticating client calls."""

    def __init__(self, app, conf):
        self._app = app
        self._init_auth_headers()

        #  TODO(aviau): auth_uri should be loaded in config
        self._auth_uri = 'www.surveil.com'

    def _init_auth_headers(self):
        """Initialize auth header list.

        Both user and service token headers are generated.
        """
        auth_headers = ['X-Service-Catalog',
                        'X-Identity-Status',
                        'X-Service-Identity-Status',
                        'X-Roles',
                        'X-Service-Roles']
        for key in six.iterkeys(_HEADER_TEMPLATE):
            auth_headers.append(key % '')
            # Service headers
            auth_headers.append(key % '-Service')

        self._auth_headers = auth_headers

    def __call__(self, env, start_response):
        """Handle incoming request.

        Authenticate send downstream on success. Reject request if
        we can't authenticate.

        """
        self._remove_auth_headers(env)

        token = self._get_header(env, 'X-Auth-Token', None)

        #  TODO(aviau): Validate token, then build proper headers
        if token == "aaaaa-bbbbb-ccccc-dddd":
            user_headers = {
                'X-Identity-Status': 'Confirmed',
                'X-User-Id': 'surveil-default-user',
                'X-Roles': 'admin,surveil',
                'X-Service-Catalog': 'surveil'
            }
            self._add_headers(env, user_headers)

            service_headers = {
                'X-Service-Identity-Status': 'Confirmed',
                'X-Service-Roles': 'surveil',
            }
            self._add_headers(env, service_headers)

        return self._call_app(env, start_response)

    def _remove_auth_headers(self, env):
        """Remove headers so a user can't fake authentication.

        Both user and service token headers are removed.

        :param env: wsgi request environment

        """
        self._remove_headers(env, self._auth_headers)

    def _remove_headers(self, env, keys):
        """Remove http headers from environment."""
        for k in keys:
            env_key = self._header_to_env_var(k)
            try:
                del env[env_key]
            except KeyError:
                pass

    def _add_headers(self, env, headers):
        """Add http headers to environment."""
        for (k, v) in six.iteritems(headers):
            env_key = self._header_to_env_var(k)
            env[env_key] = v

    def _header_to_env_var(self, key):
        """Convert header to wsgi env variable.

        :param key: http header name (ex. 'X-Auth-Token')
        :returns: wsgi env variable name (ex. 'HTTP_X_AUTH_TOKEN')

        """
        return 'HTTP_%s' % key.replace('-', '_').upper()

    def _get_header(self, env, key, default=None):
        """Get http header from environment."""
        env_key = self._header_to_env_var(key)
        return env.get(env_key, default)

    def _call_app(self, env, start_response):
        # NOTE(jamielennox): We wrap the given start response so that if an
        # application with a 'delay_auth_decision' setting fails, or otherwise
        # raises Unauthorized that we include the Authentication URL headers.
        def _fake_start_response(status, response_headers, exc_info=None):
            if status.startswith('401'):
                response_headers.extend(self._reject_auth_headers)
            return start_response(status, response_headers, exc_info)
        return self._app(env, _fake_start_response)

    def _reject_request(self, env, start_response):
        """Redirect client to auth server.

        :param env: wsgi request environment
        :param start_response: wsgi response callback
        :returns: HTTPUnauthorized http response
        """
        resp = utils.MiniResp('Authentication required',
                              env, self._reject_auth_headers)
        start_response('401 Unauthorized', resp.headers)
        return resp.body

    @property
    def _reject_auth_headers(self):
        header_val = 'Keystone uri=\'%s\'' % self._auth_uri
        return [('WWW-Authenticate', header_val)]
