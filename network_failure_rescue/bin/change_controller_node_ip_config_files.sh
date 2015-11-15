#!/usr/bin/env bash

# name : change_controller_node_ip_config_files.sh
# author : Mohammed Hannechi <mohammed.hannechi@gmail.com>
# description : This script automates the change of ip_address value in swift configuration files.
#               This is very useful in case of network failure.
# OS: Ubuntu server 14.04
# host: controller-node



ETH=$(ls /sys/class/net/ | grep ^eth)
IP=$(ip addr show $ETH | sed -n '/inet /{s/^.*inet \([0-9.]\+\).*$/\1/;p}')
HOSTNAME=$(cat /etc/hostname)
echo "IP = $IP"
echo "HOSTNAME = $HOSTNAME"

# Modify data to /etc/hosts
sudo cp /etc/hosts.bkp /etc/hosts
sudo chmod o+w /etc/hosts
sudo sed -i "/$HOSTNAME/d" /etc/hosts
sudo echo "# $HOSTNAME" >>/etc/hosts
sudo echo "$IP  $HOSTNAME" >>/etc/hosts
sudo chmod o-w /etc/hosts

# Modify data in the configuration files
sudo sed -i "/bind-address/c\bind-address = $IP" /etc/mysql/my.cnf
sudo sed -i "/connection=mysql/c\connection=mysql://keystone:swift@$IP/keystone" /etc/keystone/keystone.conf
sudo sed -i "/bind_ip/c\bind_ip = $IP" /etc/swift/proxy-server.conf


sudo swift-init proxy-server restart
echo ""

