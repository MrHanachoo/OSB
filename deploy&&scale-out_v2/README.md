This is a scalable automation deployment of a swift cluster. the environment is composed of a controller-node and multiple storage-nodes. 


controller_node
===============
The controller-node contains the authentication service (keystone) and the swift proxy-server.

* auth_service_deploy.sh :  installs and configures keystone.
	usage: $ ./auth_service_deploy.sh

* auth_test.sh : a test for keystone deployment
	usage: $ ./auth_test.sh 

* make_host_proxy_server.sh : deploys the swift proxy-server
	usage: $ ./make_host_proxy_server.sh

* create_initial_rings.sh : initialisation of the Ring(a service that  references the storage-nodes with its storage-drives)
	usage: $ ./create_initial_rings.sh <partitions_power> <replicas> <min_part_hours>
	   ex: $ ./create_initial_rings 10 3 1

* add_rings.sh : add references of new storage-nodes, including its storage drives
	usage: $ ./add_rings.sh add-rings <region_num> <zone_num> <storageNode_IPv4> <device_name> <device_weight>
	   ex: $ ./add-rings 1 1 x.x.x.x sdb1 1


storage_node
============
A storage-node contains the swift backend services that are responsible for storing, replicating, auditing objects 

* make_host_storage_node.sh : it configures the host machine as a storage node
	usage: $ ./make_host_storage_node.sh

* add_storage_drives.sh : scales the storage drives
	usage: $ ./add_storage_drives.sh <disk>
	   ex: $ ./add_storage_drives.sh sdb1 sdc1 sde1 



How to ? 
========
1) First of all, prepare the controller-node by running:
	$ ./auth_service_deploy.sh
	$ source ~/admin-openrc.sh
	$ ./make_host_proxy_server.sh
	$ ./create_initial_rings.sh <partitions_power> <replicas> <min_part_hours>

2) Prepare a storage-node:
	$ ./make_host_storage_node.sh
	$ ./plug.sh

3) Reference the storage-node with its storage-drives. On the controller-node run:
	$ ./add_ring.sh <region_num> <zone_num> <storageNode_IPv4> <device_name> <device_weight> (do this for all the devices)
    $ ./rebalance.sh
4) Distribute ring configuration files  from controller-node:
	$ cd /etc/swift
	Copy the account.ring.gz, container.ring.gz,object.ring.gz and swift.conf files to the /etc/swift directory on each storage node and any additional nodes running the proxy service.

5) On the controller-node run:
	# service proxy-server restart

6) On the storage-node run:
	# swift-init all start

Voilà, you swift cluster is ready for use.


Scaling out
===========

* Scaling drives for an existent storage node:
	- plug your hard drives and run    $ ./add_storage_drives.sh <disk>
	- add rings for those new drives, on the controller-node run   $ ./add_rings.sh <region_num> <zone_num> <storageNode_IPv4> <device_name> <device_weight>
	- distribute ring configuration files  from controller-node

* Scaling storage nodes:
	- Follow the 'how to?' section from step 2) 
    
  