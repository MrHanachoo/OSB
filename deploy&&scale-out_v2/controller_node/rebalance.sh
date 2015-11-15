#!/usr/bin/env bash

cd /etc/swift
sudo swift-ring-builder account.builder rebalance
sudo swift-ring-builder container.builder rebalance
sudo swift-ring-builder object.builder rebalance
echo '######################################################################'
echo 'NOW YOU HAVE TO COPY the *.ring.gz files to all of your storage nodes under /etc/swift directories'
exit 0