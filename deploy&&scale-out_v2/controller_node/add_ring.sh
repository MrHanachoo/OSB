#!/bin/bash

# name : add_ring.sh
# author : Mohammed Hannechi <mohammed.hannechi@gmail.com>
# description : this script adds the new storage drives to the Ring
# OS: Ubuntu server 14.04
# host: controller-node

if [[ $# -eq 5 ]]
  then
    ping -c 1 $3
    if [[ $? -eq 0 ]]
      then
        echo "$3 reachable ..."
        echo 'operating..'

      else
        echo "$3 inreachable ..."
        exit 1
    fi
  else
        echo 'USAGE: add-rings <region_num> <zone_num> <storageNode_IPv4> <device_name> <device_weight>'
    echo 'EXAMPLE: add-rings 1 1 x.x.x.x sdb1 1'
    exit 1
fi

if [[ $1 -le 3 ]]
  then 
    echo "region = $1"
  else
    echo "$1 is too much for region ref!!"
    exit 1
fi  

if [[ $2 -le 10 ]]
  then
    echo "zone = $2"
  else
    echo "$2 is too much for a zone ref !!"
    exit 1
fi

cd /etc/swift
sudo swift-ring-builder account.builder add r$1z$2-$3:6002/$4 $5
sudo swift-ring-builder container.builder add r$1z$2-$3:6001/$4 $5
sudo swift-ring-builder object.builder add r$1z$2-$3:6000/$4 $5
echo 'done.'

