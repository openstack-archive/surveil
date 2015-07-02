#!/usr/bin/env bash

sudo useradd stack
sudo bash -c "echo 'stack ALL=(ALL:ALL) NOPASSWD: ALL' >> /etc/sudoers.d/stack"
sudo git clone https://git.openstack.org/openstack-dev/devstack -b stable/juno /home/stack/devstack

# local.conf
sudo echo '[[local|localrc]]' > /home/stack/devstack/local.conf
sudo echo ADMIN_PASSWORD=password >> /home/stack/devstack/local.conf
sudo echo MYSQL_PASSWORD=password >> /home/stack/devstack/local.conf
sudo echo RABBIT_PASSWORD=password >> /home/stack/devstack/local.conf
sudo echo SERVICE_PASSWORD=password >> /home/stack/devstack/local.conf
sudo echo SERVICE_TOKEN=tokentoken >> /home/stack/devstack/local.conf
sudo echo enable_service ceilometer-acompute ceilometer-acentral ceilometer-anotification ceilometer-collector >> /home/stack/devstack/local.conf
sudo echo enable_service ceilometer-alarm-evaluator,ceilometer-alarm-notifier >> /home/stack/devstack/local.conf
sudo echo enable_service ceilometer-api >> /home/stack/devstack/local.conf
sudo echo "[[post-config|\$NOVA_CONF]]" >> /home/stack/devstack/local.conf
sudo echo "[DEFAULT]" >> /home/stack/devstack/local.conf
sudo echo notification_driver=ceilometer.compute.nova_notifier >> /home/stack/devstack/local.conf
sudo echo notification_driver=nova.openstack.common.notifier.rpc_notifier >> /home/stack/devstack/local.conf
sudo echo notification_topics=notifications,surveil >> /home/stack/devstack/local.conf
sudo echo notify_on_state_change=vm_and_task_state >> /home/stack/devstack/local.conf
sudo echo notify_on_any_change=True >> /home/stack/devstack/local.conf
sudo echo default_notification_level = INFO >> /home/stack/devstack/local.conf

sudo chown -R stack:stack /home/stack
sudo -H -u stack bash -c "cd /home/stack/devstack && ./stack.sh"
sudo iptables -F
