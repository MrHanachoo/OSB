#!/usr/bin/env bash

# name : change_storage_node_ip_config_files.sh
# author : Mohammed Hannechi <mohammed.hannechi@gmail.com>
# description : This script automates the change of ip_address value in swift configuration files.
#               This is very useful in case of network failure.
# OS: Ubuntu server 14.04
# host: storage-node

# Modify data to /etc/hosts
ETH=$(ls /sys/class/net/ | grep ^eth)
IP=$(ip addr show $ETH | sed -n '/inet /{s/^.*inet \([0-9.]\+\).*$/\1/;p}')
echo "IP = $IP"
echo "HOSTNAME = $HOSTNAME"
sudo cp /etc/hosts.bkp /etc/hosts
sudo chmod o+w /etc/hosts
read -p 'Put the controller IP address : ' IP1
echo "$IP1"
ping -c 1 $IP1
if [[ $? -eq 0 ]]
  then echo 'Controller reachable..'
else
  echo 'Controller unreachable..'
  sudo chmod o-w /etc/hosts
  exit 1
fi
sudo sed -i "/$HOSTNAME/d" /etc/hosts
sudo echo "# Controller:" >>/etc/hosts
sudo echo "$IP1  controller" >>/etc/hosts
sudo echo "# $HOSTNAME:" >>/etc/hosts
sudo echo "$IP  $HOSTNAME" >>/etc/hosts
sudo chmod o-w /etc/hosts

# Modify data in the configuration files
sudo sed -i "/address/c\address = $IP" /etc/rsyncd.conf
sudo sed -i "/bind_ip/c\bind_ip = $IP" /etc/swift/account-server.conf
sudo sed -i "/bind_ip/c\bind_ip = $IP" /etc/swift/container-server.conf
sudo sed -i "/bind_ip/c\bind_ip = $IP" /etc/swift/object-server.conf


