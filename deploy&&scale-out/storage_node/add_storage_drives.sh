#!/bin/bash

# name : add_storage_drives.sh
# author : Mohammed Hannechi <mohammed.hannechi@gmail.com>
# description : this script automate the plugging of multiple devices in a storage node
# OS: Ubuntu server 14.04
# host: storage-node



if [[ $# -eq 0 ]]
  then echo "Usage: $0 <disk>"; echo "Example: $0 sdb sdc"; exit 1
fi

# XFS utility
sudo apt-get install -y xfsprogs

for i in $*
do
  echo ""
  echo "==========="
  echo "=== $i ==="
  echo "==========="
  hdd=$i
  path=/dev/$i
  sudo fdisk -l| grep $path
  if [ $? -eq 0 ]
    then
      echo "Operating on $path ..."
        #sleep 2
    else
      echo "$path not found !!"
        exit 1
  fi

  echo "n
  p
  1


  w
  "|sudo fdisk $path

  #echo "##############################"
  path=$path'1'
  sudo mkfs.xfs -f $path

  #echo "#############################"
  if [ $? -eq 0 ]
    then
    echo "== formatting partition $path to XFS ..."
      #sleep 2
    else
      echo "Abording !"
      exit 1
  fi

  dir=/srv/node/$hdd'1'
  sudo mkdir -p $dir
  sudo chown -R swift:swift $dir
  echo "ADDING $path $dir xfs noatime,nodiratime,nobarrier,logbufs=8 0 2 TO /etc/fstab ..."
  #sleep 3
  sudo chmod o+w /etc/fstab
  echo "$path $dir xfs noatime,nodiratime,nobarrier,logbufs=8 0 2" >>/etc/fstab
  sudo chmod o-w /etc/fstab
  sudo mount $dir
  if [ $? -eq 0 ]
    then
      echo "$path mounted to $dir"
    else
      echo "mount failed !"
  fi

  echo "p
  q
  "|sudo parted /dev/$hdd
  if [[ $? -eq 0 ]]
    then echo "$i plugged successfully..."; sleep 1
    else exit 1
  fi
done
echo 'NOW YOU HAVE TO add_rings on the controller node'

