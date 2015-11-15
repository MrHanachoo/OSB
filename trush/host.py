__author__ = 'med'

import subprocess as sub
import re


class Host():
    def __init__(self):
        pass

    @staticmethod
    def get_host_ip():
        interfaces = sub.Popen(["ls", "/sys/class/net"], stdout=sub.PIPE).communicate()[0].split()
        for i in range(0, len(interfaces)):
            eth = re.search("(eth.*)", interfaces[i])
            if eth:
                return eth.group(1)

    @staticmethod
    def get_hostname():
        hostname = sub.Popen(["cat", "/etc/hostname"], stdout=sub.PIPE).communicate()[0].split()[0]
        return hostname

    @staticmethod
    def modify_hosts_file(self):
        cmd = ''
        sub.call(["sudo", "cp", "/etc/hosts", "/etc/host.bak"])
        sub.call(["sudo", "chmod", "o+x", "/etc/hosts"])
        hostname = Host.get_hostname()
        sub.call(["sudo", "sed", "-i", "/" + hostname + "/d", "/etc/hosts"])
        # sub.call(["sudo", "echo", "# "+hostname, ">>", "/etc/hosts" ])
        filename = open('/etc/hosts', 'w')
        print >> filename, "# " + hostname


'''
sudo sed -i "/$HOSTNAME/d" /etc/hosts
sudo echo "# $HOSTNAME" >>/etc/hosts
sudo echo "$IP  $HOSTNAME" >>/etc/hosts
sudo chmod o-w /etc/hosts
'''