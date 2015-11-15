__author__ = 'med'

from api import User

'''
user = User('hanachoo', 'hanachoo')
if user.exists():
    print 'exists !!!'

print user.get_ids()['tenant_id']
print user.get_ids()
'''

'''
from api import AddUser

add = AddUser('hanachoo', 'hanachoo', 'med@rosafi.com')
print add.add_user()
'''

'''
from api import Containers, Objects
cont = Containers('demo', 'demo')
l = cont.list()
print l

for i in range (0, len(l)):
    objs = Objects('demo', 'demo', l[i])
    print objs.list()
'''

'''
from api import Upload                          # didn't work !!!
path = "~/LI"
upload = Upload('demo', 'demo', 'LLL', path)
print upload.upload()
'''

'''
from api import DownloadObject

d = DownloadObject()
print d.download_object('demo', 'demo', 'CCC', 'LI')
'''
'''
from api import DownloadContainer

dc = DownloadContainer()
print dc.download_container('demo', 'demo', 'CCC')
'''
'''
import  subprocess as sub
import re
from app import app

admin_tenant = app.config['ADMIN_TENANT_NAME']
admin_username = app.config['ADMIN_USERNAME']
admin_pass = app.config['ADMIN_PASSWORD']
admin_auth_url = app.config['ADMIN_AUTH_URL']
e = sub.Popen(["keystone", "--os-tenant-name", admin_tenant, "--os-username", admin_username, "--os-password",
                         admin_pass, "--os-auth-url", admin_auth_url, "user-list"], stdout=sub.PIPE, stderr=sub.PIPE).communicate()
le = []
if not e[1]:
    l = e[0].split()
    for i in range(0, len(l)):
        bool = re.match("[^@]+@[^@]+\.[^@]+", l[i])
        if bool:
            le.append(l[i])
    print le
'''

'''
from api import AddUser

new_user = AddUser('ffff', 'fffffff', 'ffff@rosafi.com')
print new_user.add_user()
'''
'''
import subprocess as sub
import shlex
user_name = 'demo'
user_pass = 'demo'
auth_url = 'http://controller:5000/v2.0'
out = sub.Popen(["swift", "--os-tenant-name", user_name, "--os-username", user_name, "--os-password",
                         user_pass, "--os-auth-url", auth_url, "stat", "-v"], stdout=sub.PIPE, stderr=sub.PIPE).communicate()

#print out[0].split()

if not out[1]:
            index = out[0].split().index('StorageURL:')
            index1 = out[0].split().index('Token:')
            index2 = out[0].split().index('Account:')
            index3 = out[0].split().index('Containers:')
            index4 = out[0].split().index('Objects:')
            index5 = out[0].split().index('Bytes:')

            StorageURL = out[0].split()[index+1]
            Token = out[0].split()[index1+1]
            Account = out[0].split()[index2+1]
            Containers = out[0].split()[index3+1]
            Objects = out[0].split()[index4+1]
            Bytes = out[0].split()[index5+1]
            infos = {'StorageURL': StorageURL, 'Token': Token, 'Account': Account, 'Containers': Containers,
                     'Objects': Objects, 'Bytes': Bytes}
            print infos

cmd = "curl -X GET -H 'X-Auth-Token: "+infos['Token']+"' "+infos['StorageURL']+"/"

args = shlex.split(cmd)
print args
p = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()

print p[0]
'''
import subprocess as sub
import shlex
'''
from api import DeleteObject

DeleteObject.obj_del('http://controller:8080/v1/AUTH_784295f33b174134a5f81941f91ce324', 'f6119abaf3e444e0bcb1fb94545be659', 'folder2', 'demo-openrc.sh')
'''
'''
from api import DownloadObject
DownloadObject.download_object('http://controller:8080/v1/AUTH_784295f33b174134a5f81941f91ce324', 'f6119abaf3e444e0bcb1fb94545be659', 'folder2', 'api_test.py')
'''
'''
def timeout_command(command, timeout):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    import subprocess, datetime, os, time, signal
    start = datetime.datetime.now()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
      time.sleep(0.1)
      now = datetime.datetime.now()
      if (now - start).seconds> timeout:
        os.kill(process.pid, signal.SIGKILL)
        os.waitpid(-1, os.WNOHANG)
        return None
    return process.stdout.read()
from swiftclient import client
import subprocess as sub
import shlex
cmd = "curl -i -X HEAD -H 'X-Auth-Token: ec7583853a0b491fb6da1cae70eba9f6' http://controller:8080/v1/AUTH_41c2894829e1485ba518be5ac2909b43/audioBooks/jobs"
args = shlex.split(cmd)
print 'DEBUG: api.Objects.get_info().args: ' + str(args)
obj_info = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE, ).communicate()
obj_info = timeout_command(args, 1)
print 'DEBUG: api.Objects.getinfo().stderr: ' + str(obj_info[1])
print 'DEBUG: api.Objects.getinfo().strout: ' + str(obj_info[0])
'''
'''
from swiftclient import client

container_meta_data, objects_list = client.get_container('http://controller:8080/v1/AUTH_41c2894829e1485ba518be5ac2909b43', '34f4dd749b01419fab48cc4cf273433e', 'folder1', delimiter='/')

for i in range(0, len(objects_list)):
            objects_list[i]['name'] = 'folder1'+'/'+objects_list[i]['name'].decode('utf-8')
            objects_list[i]['bytes'] = objects_list[i]['bytes']/1024
            objects_list[i]['content_type'] = objects_list[i]['content_type'][12:]
            temp = objects_list[i]['last_modified'].split('T')
            #temp1 = temp.split('T')

            objects_list[i]['last_modified'] = temp[0]+" "+temp[1][:8]
            print objects_list[i]['last_modified']
'''
'''
import swiftclient

def list(url, token):

        cont_list = swiftclient.get_account(url=url, token=token)
        print type(cont_list)
        return cont_list





print list('http://controller:8080/v1/AUTH_41c2894829e1485ba518be5ac2909b43', 'fdac485d29a409cbe6f83669fd6cdd3')
'''

def check_read_acl(url='http://controller:8080/v1/AUTH_41c2894829e1485ba518be5ac2909b43', token='52f507e24bc241a1985c61af8700f8c7' , container_name='folder1'):
    cmd = "curl -X HEAD -i -H 'X-Auth-Token: " + token + "' "+ url + "/" + container_name
    args = shlex.split(cmd)
    print 'DEBUG: api.Containers.check_read_acl.args: ' + str(args)
    output = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
    print 'DEBUG: api.containers.delete.stderr: ' + str(output[1])
    print 'DEBUG: api.containers.delete.stdout: ' + str(output[0])
    try:
        index = output[0].split().index('X-Container-Read:')
        return output[0].split()[index+1]
    except ValueError:
        return False

print check_read_acl(url='http://controller:8080/v1/AUTH_41c2894829e1485ba518be5ac2909b43', token='52f507e24bc241a1985c61af8700f8c7' , container_name='g')