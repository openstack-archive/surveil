#
# Copyright 2012 New Dream Network, LLC (DreamHost)
# Copyright 2014 Hewlett-Packard Company
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

"""Access Control Lists (ACL's) control access the API server."""

from oslo_config import cfg
from oslo_policy import policy

_ENFORCER = None


policy_opts = [
    cfg.StrOpt('config_dir', default='/etc/surveil/'),
    cfg.StrOpt('config_file', default='policy.json'),
    cfg.StrOpt('project', default='surveil')
]


CONF = cfg.CONF

# We are not trying to override anything
try:
    CONF.register_opts(policy_opts)
except cfg.DuplicateOptError:
    pass


def _has_rule(name):
    return name in _ENFORCER.rules.keys()


def enforce(policy_name, request):
    """Return the user and project the request should be limited to.

    :param request: HTTP request
    :param policy_name: the policy name to validate authz against.
    """

    global _ENFORCER
    if not _ENFORCER:
        _ENFORCER = policy.Enforcer(CONF)
        _ENFORCER.load_rules()

    rule_method = "surveil:" + policy_name
    headers = request.headers

    policy_dict = dict()
    policy_dict['roles'] = headers.get('X-Roles', "").split(",")
    policy_dict['target.user_id'] = (headers.get('X-User-Id'))
    policy_dict['target.project_id'] = (headers.get('X-Project-Id'))

    # maintain backward compat with Juno and previous by allowing the action if
    # there is no rule defined for it
    if _has_rule('default') or _has_rule(rule_method):
        return _ENFORCER.enforce(rule_method, {}, policy_dict)
    else:
        return False

# TODO(fabiog): these methods are still used because the scoping part is really
# convoluted and difficult to separate out.


def get_limited_to(headers):
    """Return the user and project the request should be limited to.

    :param headers: HTTP headers dictionary
    :return: A tuple of (user, project), set to None if there's no limit on
    one of these.
    """
    global _ENFORCER
    if not _ENFORCER:
        _ENFORCER = policy.Enforcer(CONF)
        _ENFORCER.load_rules()

    policy_dict = dict()
    policy_dict['roles'] = headers.get('X-Roles', "").split(",")
    policy_dict['target.user_id'] = (headers.get('X-User-Id'))
    policy_dict['target.project_id'] = (headers.get('X-Project-Id'))

    # maintain backward compat with Juno and previous by using context_is_admin
    # rule if the segregation rule (added in Kilo) is not defined
    rule_name = 'segregation' if _has_rule(
        'segregation') else 'context_is_admin'
    if not _ENFORCER.enforce(rule_name,
                             {},
                             policy_dict):
        return headers.get('X-User-Id'), headers.get('X-Project-Id')

    return None, None


def get_limited_to_project(headers):
    """Return the project the request should be limited to.

    :param headers: HTTP headers dictionary
    :return: A project, or None if there's no limit on it.
    """
    return get_limited_to(headers)[1]
