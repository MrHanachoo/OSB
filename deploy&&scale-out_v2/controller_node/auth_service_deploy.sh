#!/bin/bash

# name : proxyServer-deploy
# author : Mohammed Hannechi <mohammed.hannechi@gmail.com>
# description : this script automate the deployment of the swift Authentification servive : code name keystone
# OS: Ubuntu server 14.04
# host: controller-node

# inject data to /etc/hosts
ETH=$(ls /sys/class/net/ | grep ^eth)
IP=$(ip addr show $ETH | sed -n '/inet /{s/^.*inet \([0-9.]\+\).*$/\1/;p}')
HOSTNAME=$(cat /etc/hostname)
echo "IP = $IP"
echo "HOSTNAME = $HOSTNAME"

sudo chmod o+w /etc/hosts
sudo sed -i "/$HOSTNAME/d" /etc/hosts
sudo cp /etc/hosts /etc/hosts.bkp
sudo echo "# $HOSTNAME" >>/etc/hosts
sudo echo "$IP  $HOSTNAME" >>/etc/hosts
sudo chmod o-w /etc/hosts

# ntp service
sudo apt-get  install -y ntp
sudo rm /var/lib/ntp/ntp.conf.dhcp
sudo service ntp restart
ntpq -c peers
ntpq -c assoc
sleep 1

# add the repo
SRT_DIR='/etc/apt/sources.list.d'
sudo chmod o+w $SRT_DIR
sudo echo "deb http://ubuntu-cloud.archive.canonical.com/ubuntu" "trusty-updates/juno main" > /$SRT_DIR/cloudarchive-juno.list
sudo chmod o-w $SRT_DIR
sudo apt-get install ubuntu-cloud-keyring
sudo apt-get update && sudo apt-get -y dist-upgrade

# Install the database server
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password swift'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password swift'
sudo apt-get install -y mariadb-server python-mysqldb
mysql -uroot -pswift -e "CREATE DATABASE keystone"
mysql -uroot -pswift -e "GRANT ALL ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'swift'"
mysql -uroot -pswift -e "GRANT ALL ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'swift'"
# Configure the database :
FILE='/etc/mysql/my.cnf'
if [ -f $FILE ]
  then
# * change the bind-address to active network interface
    sudo cp $FILE $FILE.bkp
    sudo sed -i "/bind-address/c\bind-address = $IP" $FILE
# * configure mariaDB to use UTF-8
#    sudo sed '/bind-address/a # set default collation #\
#default-storage-engine = innodb #\
#innodb_FILE_per_table #\
#collation-server = utf8_unicode_ci #\
#init-connect = '\''SET NAMES utf8'\'' #\
#character-set-server = utf8\' -i "$FILE";
  else
      echo "[ERROR] $FILE not found !"
      exit 1
fi
# restart the database service
sudo service mysql stop
sudo service mysql start
if [[ !($? -eq 0) ]]
  then
    #sudo cp $FILE.bkp $FILE
    echo 'mariaDB start failed..'
    #exit 1
fi

# secure the database service
# sudo mysql_secure_installation

sudo apt-get install ubuntu-cloud-keyring
sudo apt-get install -y keystone python-keystoneclient

# keystone conf
TOKEN=$(openssl rand -hex 30)
#echo $token
FILE1='/etc/keystone/keystone.conf'
sudo cp $FILE1 $FILE1.bkp;
sudo chmod o+rwx /etc/keystone
if [ -f $FILE1 ]
  then
    echo $FILE1...
    sudo sed -i "/admin_token/c\admin_token=$TOKEN" $FILE1
    sudo sed -i "/connection=sqlite/c\connection=mysql://keystone:swift@$IP/keystone" $FILE1
    sudo sed -i "/provider=/c\provider=keystone.token.providers.uuid.Provider" $FILE1
    sudo sed -i '/driver=keystone.to/ s/# *//' $FILE1
    sudo sed -i '/driver=keystone.contrib.re/c\driver=keystone.contrib.revoke.backends.sql.Revoke' $FILE1
    sudo sed -i '/verbose=/c\verbose=True' $FILE1
  else
    echo "[ERROR] $FILE1 not found !"
    #sudo cp $FILE.bkp $FILE;
    #sudo cp $FILE1.bkp $FILE1;
    mysql -u root -pswift -e "DROP DATABASE keystone;"
    sudo chmod o-rwx /etc/keystone
    exit 1
fi
sudo chmod o-rwx /etc/keystone
# populate the keystone database
sudo keystone-manage db_sync

if [ $? -eq 0 ]
  then
    echo "keystone database populated successfully..."
  else
    echo "[ERROR] keystone database population failed... "
    #sudo cp $FILE.bkp $FILE;
    #sudo cp $FILE1.bkp $FILE1;
    #mysql -u root -pswift -e "DROP DATABASE keystone;"
    exit 1
fi
sudo service keystone restart
# delete the default SQLite keystone database
sudo rm -f /var/lib/keystone/keystone.db

# purge expired token hourly
# sudo (crontab -l -u keystone 2>&1 | grep -q token_flush) || \
#  echo '@hourly /usr/bin/keystone-manage token_flush >/var/log/keystone/keystone-tokenflush.log 2>&1' \
#  >> /var/spool/cron/crontabs/keystone

# get admin_token value from /etc/keystone/keystone.conf
TEMP=$(sudo grep admin_token $FILE1)
TOKEN1=(${TEMP//admin_token=/})
echo $TOKEN
echo $TOKEN1
echo "export OS_SERVICE_TOKEN=$TOKEN1" >~/auth-openrc.sh
echo "export OS_SERVICE_ENDPOINT=http://$HOSTNAME:35357/v2.0" >>~/auth-openrc.sh

# auth service config

# create the admin tenant
keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 tenant-create --name admin --description "Admin Tenant"
# create the user
read -p 'Choose a password for the admin user: ' -s ADMIN_PASS
echo ''
read -p 'Put the admin email : ' ADMIN_EMAIL
keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 user-create --name admin --pass $ADMIN_PASS --email $ADMIN_EMAIL
# create the admin role
keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 role-create --name admin
# add admin role to the admin user within admin tenant
keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 user-role-add --user admin --tenant admin --role admin
# create the demo tenant
keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 tenant-create --name demo --description "Demo Tenant"
# ceate the demo user
read -p 'Choose a password for the demo user: ' -s DEMO_PASS
echo ''
read -p 'Put the demo email : ' DEMO_EMAIL
keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 user-create --name demo --tenant demo --pass $DEMO_PASS --email $DEMO_EMAIL
# create the tenant service
keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 tenant-create --name service --description "Service Tenant"
# create the service identity
keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 service-create --name keystone --type identity --description " Identity Service"
# create identity API endpoint
ID=$(keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 service-list | awk '/ identity / {print $2}')
keystone --os-token $TOKEN1 --os-endpoint http://$HOSTNAME:35357/v2.0 endpoint-create --service-id $ID --publicurl http://$HOSTNAME:5000/v2.0 --internalurl http://$HOSTNAME:5000/v2.0 --adminurl http://$HOSTNAME:35357/v2.0 --region region_1

# auth service test

read -p 'Enter the admin password : ' -s ADMIN_PASS
keystone --os-tenant-name admin --os-username admin --os-password $ADMIN_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 token-get
keystone --os-tenant-name admin --os-username admin --os-password $ADMIN_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 tenant-list
keystone --os-tenant-name admin --os-username admin --os-password $ADMIN_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 user-list
keystone --os-tenant-name admin --os-username admin --os-password $ADMIN_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 role-list


read -p 'Enter the demo password : ' -s DEMO_PASS
keystone --os-tenant-name demo --os-username demo --os-password $DEMO_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 token-get
keystone --os-tenant-name demo --os-username demo --os-password $DEMO_PASS --os-auth-url http://$HOSTNAME:35357/v2.0 user-list
echo ' # You see ! Only the admin has the right to manage keystone components.'
echo  '# done.'


echo 'export OS_TENANT_NAME=admin' > ~/admin-openrc.sh
echo 'export OS_USERNAME=admin' >> ~/admin-openrc.sh
echo "export OS_PASSWORD=$ADMIN_PASS"  >> ~/admin-openrc.sh
echo "export OS_AUTH_URL=http://$HOSTNAME:35357/v2.0" >> ~/admin-openrc.sh

echo 'export OS_TENANT_NAME=demo' > ~/demo-openrc.sh
echo 'export OS_USERNAME=demo' >> ~/demo-openrc.sh
echo "export OS_PASSWORD=$DEMO_PASS" >> ~/demo-openrc.sh
echo "export OS_AUTH_URL=http://$HOSTNAME:5000/v2.0" >> ~/demo-openrc.sh



echo '############################################'
echo '# auth_server deployed succcesfully.'
echo '# root database password : swift (if you want to change it run # mysql_secure_installation)'
echo '# keystone database passwors : swift '
echo '# run: $ source ~/admin-openrc.sh'
echo '# run: $ ./make_host_proxy_server'
echo '# done.'



