#!/bin/bash

# name : make_host_proxy_deploy.sh
# author : Mohammed Hannechi <mohammed.hannechi@gmail.com>
# description : this script deploys the swift proxy-server on the controller node
# OS: Ubuntu server 14.04
# host: controller-node

# Create the swift user:
read -p 'Choose a password for the swift user : ' -s SWIFT_PASS
keystone user-create --name swift --pass $SWIFT_PASS

# Add the admin role to the swift user:
keystone user-role-add --user swift --tenant service --role admin

# Create the swift service entity:
keystone service-create --name swift --type object-store --description "Object Storage"

# Create the Object Storage service API endpoints:
HOSTNAME=$(cat /etc/hostname)
keystone endpoint-create --service-id $(keystone service-list | awk '/ object-store / {print $2}') --publicurl "http://$HOSTNAME:8080/v1/AUTH_%(tenant_id)s" --internalurl "http://$HOSTNAME:8080/v1/AUTH_%(tenant_id)s" --adminurl http://$HOSTNAME:8080 --region regionOne

#  Install the packages:
sudo apt-get -y install swift swift-proxy python-swiftclient python-keystoneclient python-keystonemiddleware memcached

# Create the /etc/swift directory:
sudo mkdir /etc/swift

# Obtain the proxy service configuration file from the Object Storage source repository:
sudo curl -o /etc/swift/proxy-server.conf https://raw.githubusercontent.com/openstack/swift/stable/juno/etc/proxy-server.conf-sample

ETH=$(ls /sys/class/net/ | grep ^eth)
IP=$(ip addr show $ETH | sed -n '/inet /{s/^.*inet \([0-9.]\+\).*$/\1/;p}')

# /etc/swift/proxy-server.conf file
FILE=/etc/swift/proxy-server.conf
sudo cp $FILE $FILE.bkp
# [DEFAULT]
sudo sed -i "/bind_ip/c\bind_ip = $IP" $FILE
sudo sed -i '/bind_port/ s/# *//' $FILE
sudo sed -i '/user = swift/ s/# *//' $FILE
sudo sed -i '/swift_dir/ s/# *//' $FILE
# Enable the appropriate modules in the [pipeline:main] section:
# [pipeline:main]
sudo sed -i '/pipeline =/c\pipeline =  cache healthcheck tempurl authtoken keystoneauth proxy-logging proxy-server' $FILE
# Enable account management in the [management:proxy-server] section:
# [management:proxy-server]
sudo sed -i '/allow_account_management/c\allow_account_management = true' $FILE
sudo sed -i '/account_autocreate/c\account_autocreate = true' $FILE
# Configure the operator roles in the [filter:keystoneauth] section:
# [filter:keystoneauth]
sudo sed -i '/filter:keystoneauth/s/# *//' $FILE
sudo sed -i '/egg:swift#keystoneauth/s/# *//' $FILE
sudo sed -i '/operator_roles/c\operator_roles = admin,_member_' $FILE
# Configure Identity service access in the [filter:authtoken] section:
# [filter:authtoken]
sudo sed -i '/filter:authtoken/s/# *//' $FILE
sudo sed -i '/paste.filter_factory/s/# *//' $FILE
sudo sed -i "/auth_uri/c\auth_uri = http://$HOSTNAME:5000/v2.0" $FILE
sudo sed -i "/auth_host/c\auth_host = $HOSTNAME" $FILE
sudo sed -i '/auth_port/s/# *//' $FILE
sudo sed -i '/auth_protocol/s/# *//' $FILE
sudo sed -i '/admin_tenant_name/s/# *//' $FILE
sudo sed -i '/admin_user/s/# *//' $FILE
sudo sed -i "/admin_password/c\admin_password = $SWIFT_PASS" $FILE
sudo sed -i '/delay_auth_decision/c\delay_auth_decision = true' $FILE

# Configure the memcached location in the [filter:cache] section:
# [filter:cache]
sudo sed -i '/memcache_servers =/s/# *//' $FILE

# Obtain the /etc/swift/swift.conf file from the Object Storage source repository:
sudo curl -o /etc/swift/swift.conf https://raw.githubusercontent.com/openstack/swift/stable/juno/etc/swift.conf-sample

PREFIX=$(openssl rand -hex 30)
SUFFIX=$(openssl rand -hex 30)

# /etc/swift/swift.conf file
FILE1=/etc/swift/swift.conf
sudo cp $FILE1 $FILE1.bkp
# [swift-hash]
sudo sed -i "/swift_hash_path_suffix =/c\swift_hash_path_suffix = $SUFFIX" $FILE1
sudo sed -i "/swift_hash_path_prefix =/c\swift_hash_path_prefix = $PREFIX" $FILE1

# [storage-policy:0]
# name = Policy-0
# default = yes

sudo chown -R swift:swift /etc/swift
sudo service memcached restart

echo '# done.'
echo '##################################'
echo '# run : ./create_initial_rings.sh'

