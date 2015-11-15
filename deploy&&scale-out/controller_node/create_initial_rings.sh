#!/bin/bash

# name : create_initial_rings.sh
# author : Mohammed Hannechi <mohammed.hannechi@gmail.com>
# description : this script builds the inital Rings
# OS: Ubuntu server 14.04
# host: controller-node

if [[ !($# -eq 3) ]]
	then
		echo 'USAGE: create_initial_rings <partitions_power> <replicas> <min_part_hours>'
    	echo 'EXAMPLE: create_initial_rings 10 3 1'
    	exit 1
fi

cd /etc/swift
sudo swift-ring-builder account.builder create $1 $2 $3
sudo swift-ring-builder container.builder create $1 $2 $3
sudo swift-ring-builder object.builder create $1 $2 $3
echo 'done.'
echo 'NOW YOU HAVE TO add_rings'