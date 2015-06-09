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

"""Starter script for the surveil openstack interface"""

from __future__ import print_function

import json
import os
import sys
import threading
import time

import pika
from six.moves import configparser
from surveilclient import client


def main():
    config = configparser.ConfigParser()
    config.read("/etc/surveil/surveil_os_interface.cfg")

    daemon_config = {
        "SURVEIL_API_URL": os.environ.get(
            'SURVEIL_API_URL',
            config.get("surveil-os-interface", "SURVEIL_API_URL")
        ),
        "SURVEIL_AUTH_URL": os.environ.get(
            'SURVEIL_AUTH_URL',
            config.get("surveil-os-interface", "SURVEIL_AUTH_URL")
        ),
        "SURVEIL_VERSION": os.environ.get(
            'SURVEIL_VERSION',
            config.get("surveil-os-interface", "SURVEIL_VERSION")
        ),
        "RABBIT_HOST": os.environ.get(
            'RABBIT_HOST',
            config.get("surveil-os-interface", "RABBIT_HOST")
        ),
        "RABBIT_PORT": int(os.environ.get(
            'RABBIT_PORT',
            config.get("surveil-os-interface", "RABBIT_PORT")
        )
        ),
        "QUEUE": os.environ.get(
            'QUEUE',
            config.get("surveil-os-interface", "QUEUE")
        ),
        "RABBIT_USER": os.environ.get(
            'RABBIT_USER',
            config.get("surveil-os-interface", "RABBIT_USER")
        ),
        "RABBIT_PASSWORD": os.environ.get(
            'RABBIT_PASSWORD',
            config.get("surveil-os-interface", "RABBIT_PASSWORD")
        ),
        "SURVEIL_OS_AUTH_URL": os.environ.get(
            'SURVEIL_OS_AUTH_URL',
            config.get("surveil-os-interface", "SURVEIL_OS_AUTH_URL")
        ),
        "SURVEIL_OS_USERNAME": os.environ.get(
            'SURVEIL_OS_USERNAME',
            config.get("surveil-os-interface", "SURVEIL_OS_USERNAME")
        ),
        "SURVEIL_OS_PASSWORD": os.environ.get(
            'SURVEIL_OS_PASSWORD',
            config.get("surveil-os-interface", "SURVEIL_OS_PASSWORD")
        ),
        "SURVEIL_OS_TENANT_NAME": os.environ.get(
            'SURVEIL_OS_TENANT_NAME',
            config.get("surveil-os-interface", "SURVEIL_OS_TENANT_NAME")
        ),
        "SURVEIL_DEFAULT_TAGS": os.environ.get(
            'SURVEIL_DEFAULT_TAGS',
            config.get("surveil-os-interface", "SURVEIL_DEFAULT_TAGS")
        ),
        "SURVEIL_NETWORK_LABEL": os.environ.get(
            'SURVEIL_NETWORK_LABEL',
            config.get("surveil-os-interface", "SURVEIL_NETWORK_LABEL")
        ),
    }

    if (daemon_config["RABBIT_USER"] is not None
            and daemon_config["RABBIT_PASSWORD"] is not None):
        id = pika.credentials.PlainCredentials(
            daemon_config["RABBIT_USER"],
            daemon_config["RABBIT_PASSWORD"]
        )

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=daemon_config["RABBIT_HOST"],
                port=daemon_config["RABBIT_PORT"],
                credentials=id
            )
        )
    else:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=daemon_config["RABBIT_HOST"],
                port=daemon_config["RABBIT_PORT"]
            )
        )

    channel = connection.channel()
    channel.queue_declare(queue=daemon_config["QUEUE"])

    threads = []
    compt_thread = []

    def reload_config_threads():
        c = client.Client(daemon_config["SURVEIL_API_URL"],
                          auth_url=daemon_config["SURVEIL_AUTH_URL"],
                          version=daemon_config["SURVEIL_VERSION"])
        while True:
            time.sleep(30)
            if compt_thread:
                c.config.reload_config()
                del (compt_thread[:])

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

    reload_config_thread = threading.Thread(target=reload_config_threads)
    reload_config_thread.daemon = True
    reload_config_thread.start()

    def process_instance_create_start(event, sclient):
            custom_fields = {
                "_OS_AUTH_URL": daemon_config["SURVEIL_OS_AUTH_URL"],
                "_OS_TENANT_NAME": daemon_config["SURVEIL_OS_TENANT_NAME"],
                "_OS_USERNAME": daemon_config["SURVEIL_OS_USERNAME"],
                "_OS_PASSWORD": daemon_config["SURVEIL_OS_PASSWORD"],
                "_OS_INSTANCE_ID": event['payload']['instance_id']
            }

            surveil_metadata_custom_fields = event['payload']['metadata'].get(
                'surveil_custom_fields',
                None
            )

            #  Custom fields
            if surveil_metadata_custom_fields is not None:
                try:
                    custom_fields.update(
                        json.loads(surveil_metadata_custom_fields)
                    )
                except ValueError:
                    print("Could not load json %s" %
                          surveil_metadata_custom_fields,
                          file=sys.stderr)

            # Tags
            instance_tags = daemon_config["SURVEIL_DEFAULT_TAGS"]
            surveil_metadata_tags = event['payload']['metadata'].get(
                'surveil_tags',
                None
            )
            if surveil_metadata_tags is not None:
                instance_tags += ',' + surveil_metadata_tags

            sclient.config.hosts.create(
                host_name=event['payload']['hostname'],
                address=event['payload']['hostname'],
                use=instance_tags,
                custom_fields=custom_fields
            )

    def process_instance_create_end(event, sclient):
        #  Get the ip address
        addresses = event['payload'].get('fixed_ips', [])
        for addr in addresses:
            if (addr.get('label', '') ==
                    daemon_config['SURVEIL_NETWORK_LABEL']):
                sclient.config.hosts.update(
                    event['payload']['hostname'],
                    address=addr['address']
                )
                break

    def process_instance_delete_end(sclient, event):
        sclient.config.hosts.delete(event['payload']['hostname'])

    def process_event(body):
        sclient = client.Client(daemon_config["SURVEIL_API_URL"],
                                auth_url=daemon_config["SURVEIL_AUTH_URL"],
                                version=daemon_config["SURVEIL_VERSION"])

        #  Load the event
        event = json.loads(body)

        #  Process the event
        try:
            if event['event_type'] == 'compute.instance.create.start':
                process_instance_create_start(event, sclient)
            elif event['event_type'] == 'compute.instance.create.end':
                process_instance_create_end(event, sclient)
            elif event['event_type'] == 'compute.instance.delete.end':
                process_instance_delete_end(sclient, event)
        except Exception as e:
            print("Could not process event %s" % e, file=sys.stderr)

    def callback(ch, method, properties, body):
        t = threading.Thread(target=process_event, args=(body,))
        t.daemon = True
        t.start()
        threads.append(t)
        compt_thread.append(t)

    channel.basic_consume(callback, queue=daemon_config["QUEUE"], no_ack=True)
    channel.start_consuming()
