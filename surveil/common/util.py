#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from functools import wraps

from webob import exc
import pecan


# TODO(aviau && maybe Freddrickk): Properly document this decorator dudeasdasfd
def policy_enforce(actions):
    def policy_enforce_inner(handler):
        def handle_stack_method(controller, **kwargs):
            context = pecan.request.context
            print('salut', context)
            for action in actions:
                allowed = context.policy.enforce(context=context,
                                                 action=action,
                                                 scope=context.REQUEST_SCOPE)
                if not allowed:
                    raise exc.HTTPForbidden()

            return handler(controller, **kwargs)
        return handle_stack_method
    return policy_enforce_inner
