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

import json
import os
import threading
import time

import pika
from six.moves import configparser
from surveilclient import client


def main():
    config = configparser.ConfigParser()
    config.read("/etc/surveil/surveil_rabbitMQ_consummer.cfg")

    daemon_config = {
        "SURVEIL_API_URL": os.environ.get(
            'SURVEIL_API_URL',
            config.get("surveilRabbitMQConsummer", "SURVEIL_API_URL")
        ),
        "SURVEIL_AUTH_URL": os.environ.get(
            'SURVEIL_AUTH_URL',
            config.get("surveilRabbitMQConsummer", "SURVEIL_AUTH_URL")
        ),
        "SURVEIL_VERSION": os.environ.get(
            'SURVEIL_VERSION',
            config.get("surveilRabbitMQConsummer", "SURVEIL_VERSION")
        ),
        "RABBIT_HOST": os.environ.get(
            'RABBIT_HOST',
            config.get("surveilRabbitMQConsummer", "RABBIT_HOST")
        ),
        "RABBIT_PORT": int(os.environ.get(
            'RABBIT_PORT',
            config.get("surveilRabbitMQConsummer", "RABBIT_PORT")
        )
        ),
        "QUEUE": os.environ.get(
            'QUEUE',
            config.get("surveilRabbitMQConsummer", "QUEUE")
        ),
        "RABBIT_USER": os.environ.get(
            'RABBIT_USER',
            config.get("surveilRabbitMQConsummer", "RABBIT_USER")
        ),
        "RABBIT_PASSWORD": os.environ.get(
            'RABBIT_PASSWORD',
            config.get("surveilRabbitMQConsummer", "RABBIT_PASSWORD")
        ),
        "OS_AUTH_URL": os.environ.get(
            'OS_AUTH_URL',
            config.get("surveilRabbitMQConsummer", "OS_AUTH_URL")
        ),
        "OS_USERNAME": os.environ.get(
            'OS_USERNAME',
            config.get("surveilRabbitMQConsummer", "OS_USERNAME")
        ),
        "OS_PASSWORD": os.environ.get(
            'OS_PASSWORD',
            config.get("surveilRabbitMQConsummer", "OS_PASSWORD")
        )
    }

    if (daemon_config["RABBIT_USER"] is not None
            and daemon_config["RABBIT_PASSWORD"] is not None):
        id = pika.credentials.PlainCredentials(daemon_config["RABBIT_USER"],
                                               daemon_config["RABBIT_PASSWORD"]
                                               )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=daemon_config["RABBIT_HOST"],
                                      port=daemon_config["RABBIT_PORT"],
                                      credentials=id))
    else:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=daemon_config["RABBIT_HOST"],
                                      port=daemon_config["RABBIT_PORT"]))

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

    def process_event(body):
        c = client.Client(daemon_config["SURVEIL_API_URL"],
                          auth_url=daemon_config["SURVEIL_AUTH_URL"],
                          version=daemon_config["SURVEIL_VERSION"])
        event = json.loads(body)
        if event['event_type'] == 'compute.instance.create.start':
            custom_fields = {
                "_OS_AUTH_URL": daemon_config["OS_AUTH_URL"],
                "_OS_TENANT_NAME": '8979',
                "_OS_USERNAME": daemon_config["OS_USERNAME"],
                "_OS_PASSWORD": daemon_config["OS_PASSWORD"],
                "_OS_INSTANCE_ID": event['payload']['instance_id']
            }
            c.config.hosts.create(
                host_name=event['payload']['hostname'],
                address=event['payload']['hostname'],
                use='linux-openstackceilometer',
                custom_fields=custom_fields
            )
        if event['event_type'] == 'compute.instance.delete.end':
            c.config.hosts.delete(event['payload']['hostname'])

    def callback(ch, method, properties, body):
        t = threading.Thread(target=process_event, args=(body,))
        t.daemon = True
        t.start()
        threads.append(t)
        compt_thread.append(t)

    channel.basic_consume(callback, queue=daemon_config["QUEUE"], no_ack=True)
    channel.start_consuming()