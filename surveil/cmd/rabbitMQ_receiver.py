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
import argparse
import json
import sys
import threading
import time

import pika
from surveilclient import client


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog='surveil-rabbitMQ-receiver',
        add_help=False,
    )
    parser.add_argument('--surveil-url',
                        default='http://localhost:8080/v2',
                        help='Defaults to http://localhost:8080/v2', type=str)
    parser.add_argument('--surveil-auth-url',
                        default='http://localhost:8080/v2/auth',
                        help='Defaults to http://localhost:8080/v2/auth',
                        type=str)
    parser.add_argument('--surveil-version',
                        default='2_0',
                        help='Defaults to 2_0', type=str)
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
    parser.add_argument('--os-auth-url',
                        default='admin',
                        help='OS_AUTH_URL', type=str)
    parser.add_argument('--os-username',
                        default='admin',
                        help='OS_USERNAME', type=str)
    parser.add_argument('--os-password',
                        default='admin',
                        help='OS_PASSWORD', type=str)

    (options, args) = parser.parse_known_args(sys.argv[1:])

    if (options.rabbit_user is not None
            and options.rabbit_password is not None):
        id = pika.credentials.PlainCredentials(options.rabbit_user,
                                               options.rabbit_password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=options.rabbit_host,
                                      port=options.rabbit_port,
                                      credentials=id))

    else:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=options.rabbit_host,
                                      port=options.rabbit_port))

    channel = connection.channel()
    channel.queue_declare(queue=options.queue)

    threads = []

    def join_finished_threads():
        while True:
            time.sleep(1)
            todel = []
            for t in threads:
                if not t.isAlive():
                    t.join()
                    todel.append(t)
            for t in todel:
                threads.remove(t)

    joiner_thread = threading.Thread(target=join_finished_threads)
    joiner_thread.daemon = True
    joiner_thread.start()

    def command_host(body):
        c = client.Client(options.surveil_url,
                          auth_url=options.surveil_auth_url,
                          version=options.surveil_version)
        d = json.loads(body)
        if d['event_type'] == 'compute.instance.create.start':
            custom_fields = {
                "_OS_AUTH_URL": options.os_auth_url,
                "_OS_TENANT_NAME": '8979',
                "_OS_USERNAME": options.os_username,
                "_OS_PASSWORD": options.os_password,
                "_OS_INSTANCE_ID": d['payload']['instance_id']
            }

            c.config.hosts.create(
                host_name=d['payload']['hostname'],
                address=d['payload']['hostname'],
                use='linux-openstackceilometer',
                custom_fields=custom_fields
            )

        if d['event_type'] == 'compute.instance.delete.end':
            c.config.hosts.delete(d['payload']['hostname'])

    def callback(ch, method, properties, body):
        t = threading.Thread(target=command_host, args=(body,))
        t.daemon = True
        t.start()
        threads.append(t)

    channel.basic_consume(callback, queue=options.queue, no_ack=True)
    channel.start_consuming()