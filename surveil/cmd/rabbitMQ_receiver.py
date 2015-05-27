# Copyright 2014 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Starter script for the RabbitMQ receiver"""
from surveilclient import client

import argparse
import json
import pika
import sys
import thread


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog='surveil-rabbitMQ-receiver',
        add_help=False,
    )
    parser.add_argument('--rabbit-host',
                        default='localhost',
                        help='Defaults to localhost', type=str)
    parser.add_argument('--rabbit-port',
                        default=5672,
                        help='Defaults to 5672', type=int)
    parser.add_argument('queue', type=str, help='Rabbit Queue')
    parser.add_argument('--rabbit-user',
                        default=None,
                        help='Rabbit user', type=str)
    parser.add_argument('--rabbit-password',
                        default=None,
                        help='Rabbit password', type=str)

    (options, args) = parser.parse_known_args(sys.argv[1:])

    if options.rabbit_user is not None and options.rabbit_password is not None:
        id = pika.credentials.PlainCredentials(options.rabbit_user, options.rabbit_password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=options.rabbit_host, port=options.rabbit_port,
                                      credentials=id))
    else:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=options.rabbit_host, port=options.rabbit_port))

    channel = connection.channel()
    channel.queue_declare(queue=options.queue)

    def command_host( body):
        c = client.Client('http://localhost:8080/v2',
                  auth_url='http://localhost:8080/v2/auth',
                  version='2_0')
        print " [x] Received %r" % (body,)
        print(type(body))
        d = json.loads(body)
        if d['event_type'] == 'compute.instance.create.start':
            print('CREATION')
            url = "127.0.0.1"
            print(url)
            print(d['payload']['hostname'])
            print(d['_context_project_name'])
            print(options.rabbit_user)
            print(options.rabbit_password)
            print(d['payload']['instance_id'])
            custom_fields = ('{"_OS_AUTH_URL":"%s",'
                             ' "_OS_TENANT_NAME":"%s",'
                             ' "_OS_USERNAME":"%s",'
                             ' "_OS_PASSWORD":"%s",'
                             ' "_OS_INSTANCE_ID": "%s"}' % (url, d['_context_project_name'], options.rabbit_user,
                                                            options.rabbit_password, d['payload']['instance_id']))

            c.hosts.create(hostname=d['payload']['hostname'], address=url, use='linux-openstackceilometer',
                                custom_fields=custom_fields)
        if d['event_type'] == 'compute.instance.delete.end':
            print('DESTRUCTION')
            c.hosts.delete(d['payload']['hostname'])

    def callback(ch, method, properties, body):
        thread.start_new_thread(command_host, (body,))

    channel.basic_consume(callback, queue=options.queue, no_ack=True)
    channel.start_consuming()

