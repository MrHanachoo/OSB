#!/bin/bash

# name : auth_test.sh
# author : Mohammed Hannechi <mohammed.hannechi@gmail.com>
# description : this script tests the deployment of the swift Authentification servive : code name keystone
# OS: Ubuntu server 14.04
# host: controller-node


unset OS_SERVICE_TOKEN OS_SERVICE_ENDPOINT
HOSTNAME=$(cat /etc/hostname)

read -p 'Enter the admin password : ' -s ADMIN_PASS
keystone --os-tenant-name admin --os-username admin --os-password $ADMIN_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 token-get
keystone --os-tenant-name admin --os-username admin --os-password $ADMIN_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 tenant-list
keystone --os-tenant-name admin --os-username admin --os-password $ADMIN_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 user-list
keystone --os-tenant-name admin --os-username admin --os-password $ADMIN_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 role-list


read -p 'Enter the demo password : ' -s DEMO_PASS
keystone --os-tenant-name demo --os-username demo --os-password $DEMO_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 token-get
keystone --os-tenant-name demo --os-username demo --os-password $DEMO_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 user-list
echo 'You see ! Only the admin has the right to manage keystone components.'
echo  'done.'


echo 'export OS_TENANT_NAME=admin' > ~/admin-openrc.sh
echo 'export OS_USERNAME=admin' >> ~/admin-openrc.sh
echo "export OS_PASSWORD=$ADMIN_PASS"  >> ~/admin-openrc.sh
echo "export OS_AUTH_URL=http://$HOSTNAME:35357/v2.0" >> ~/admin-openrc.sh

echo 'export OS_TENANT_NAME=demo' > ~/demo-openrc.sh
echo 'export OS_USERNAME=demo' >> ~/demo-openrc.sh
echo "export OS_PASSWORD=$DEMO_PASS" >> ~/demo-openrc.sh
echo "export OS_AUTH_URL=http://$HOSTNAME:5000/v2.0" >> ~/demo-openrc.sh
