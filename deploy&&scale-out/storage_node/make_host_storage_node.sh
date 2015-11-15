#!/bin/bash

# name : make_host_storage_node.sh
# author : Mohammed Hannechi <mohammed.hannechi@gmail.com>
# description : this script automate the deployment of a storage node
# OS: Ubuntu server 14.04
# host: storage-node 


# Prevention from running the script another time, once the host is configured as storage node
if [[ -d /etc/swift ]]
  then
    OWNER=$(stat -c "%U" /etc/swift/)
    if [[ $OWNER = swift ]]
      then
        echo "This host is already a STORAGE NODE."
        exit 1
    fi
fi

# inject data to /etc/hosts
ETH=$(ls /sys/class/net/ | grep ^eth)
IP=$(ip addr show $ETH | sed -n '/inet /{s/^.*inet \([0-9.]\+\).*$/\1/;p}')
HOSTNAME=$(cat /etc/hostname)
echo "IP = $IP"
echo "HOSTNAME = $HOSTNAME"
sudo cp /etc/hosts /etc/hosts.bkp
sudo chmod o+w /etc/hosts
read -p 'Put the controller IP address : ' IP1
echo "$IP1"
ping -c 1 $IP1
if [[ $? -eq 0 ]]
  then echo 'Controller reachable..'
else
  echo 'Controller unreachable..'; sudo chmod o-w /etc/hosts; exit 1
fi
sudo sed -i "/$HOSTNAME/d" /etc/hosts
sudo echo "# Controller:" >>/etc/hosts
sudo echo "$IP1  controller" >>/etc/hosts
sudo echo "# $HOSTNAME:" >>/etc/hosts
sudo echo "$IP  $HOSTNAME" >>/etc/hosts
sudo chmod o-w /etc/hosts

# Config ntp
sudo apt-get install -y ntp
#sudo cp /etc/ntp.conf /etc/ntp.conf.bkp
sudo service ntp restart
ntpq -c peers
ntpq -c assoc
sleep 1

# add the repo
sudo apt-get install ubuntu-cloud-keyring
SRT_DIR=/etc/apt/sources.list.d
sudo chmod o+w $SRT_DIR
sudo echo "deb http://ubuntu-cloud.archive.canonical.com/ubuntu" "trusty-updates/juno main" > /$SRT_DIR/cloudarchive-juno.list
sudo chmod o-w $SRT_DIR
sudo apt-get update && apt-get dist-upgrade

# Install the supporting utility packages:
sudo apt-get install -y  rsync
# Inject some data to rsyncd.conf
FILE=/etc/rsyncd.conf
sudo touch $FILE
sudo chmod o+w $FILE
sudo echo 'uid = swift' >$FILE
if [[ $? -eq 0 ]]
  then echo "Configuring $FILE ..."
  sleep 1
else
  sudo cp /etc/hosts.bkp /etc/hosts
  exit 1
fi
sudo echo 'gid = swift' >>$FILE
sudo echo 'log file = /var/log/rsyncd.log' >>$FILE
sudo echo 'pid file = /var/run/rsyncd.pid' >>$FILE
sudo echo "address = $IP" >>$FILE
sudo echo '' >>$FILE
sudo echo '[account]' >>$FILE
sudo echo 'max connections = 50' >>$FILE
sudo echo 'path = /srv/node/' >>$FILE
sudo echo 'read only = false' >>$FILE
sudo echo 'lock file = /var/lock/account.lock' >>$FILE
sudo echo '' >>$FILE
sudo echo '[container]' >>$FILE
sudo echo 'max connections = 50' >>$FILE
sudo echo 'path = /srv/node/' >>$FILE
sudo echo 'read only = false' >>$FILE
sudo echo 'lock file = /var/lock/container.lock' >>$FILE
sudo echo '' >>$FILE
sudo echo '[object]' >>$FILE
sudo echo 'max connections = 50' >>$FILE
sudo echo 'path = /srv/node/' >>$FILE
sudo echo 'read only = false' >>$FILE
sudo echo 'lock file = /var/lock/object.lock' >>$FILE
sudo chmod o-w $FILE
# Edit /etc/default/rsync :
sudo sed -i "/RSYNC_ENABLE/c\RSYNC_ENABLE=true" /etc/default/rsync
sudo service rsync start

# Install&configure storage node components:
ACC=/etc/swift/account-server.conf
CONT=/etc/swift/container-server.conf
OBJ=/etc/swift/object-server.conf
sudo apt-get install -y swift swift-account swift-container swift-object
sudo curl -o $ACC https://raw.githubusercontent.com/openstack/swift/stable/juno/etc/account-server.conf-sample
sudo curl -o $CONT https://raw.githubusercontent.com/openstack/swift/stable/juno/etc/container-server.conf-sample
sudo curl -o $OBJ https://raw.githubusercontent.com/openstack/swift/stable/juno/etc/object-server.conf-sample

# Edit the /etc/swift/account-server.conf
sudo cp $ACC $ACC.bkp
# [default]
sudo sed -i "/bind_ip/c\bind_ip = $IP" $ACC
sudo sed -i '/user =/ s/# *//' $ACC
sudo sed -i '/swift_dir/ s/# *//' $ACC
sudo sed -i '/devices/ s/# *//' $ACC
# [pipeline:main]
###
# [filter:recon]
sudo sed -i '/recon_cache_path/ s/# *//' $ACC

# Edit the /etc/swift/container-server.conf
sudo cp $CONT $CONT.bkp
# [DEFAULT]
sudo sed -i "/bind_ip/c\bind_ip = $IP" $CONT
sudo sed -i '/user =/ s/# *//' $CONT
sudo sed -i '/swift_dir/ s/# *//' $CONT
sudo sed -i '/devices/ s/# *//' $CONT
# [pipeline:main]
###
# [filter:recon]
sudo sed -i '/recon_cache_path/ s/# *//' $CONT

# Edit the /etc/swift/object-server.conf
sudo cp $OBJ $OBJ.bkp
# [DEFAULT]
sudo sed -i "/bind_ip/c\bind_ip = $IP" $OBJ
sudo sed -i '/user =/ s/# *//' $OBJ
sudo sed -i '/swift_dir/ s/# *//' $OBJ
sudo sed -i '/devices/ s/# *//' $OBJ
# [pipeline:main]
###
# [filter:recon]
sudo sed -i '/recon_cache_path/ s/# *//' $OBJ

sudo chown -R swift:swift /srv/node
sudo mkdir -p /var/cache/swift
sudo chown -R swift:swift /var/cache/swift
echo 'done.'
echo '######################################################################'
echo 'NOW YOU HAVE TO add-storage-drives'

