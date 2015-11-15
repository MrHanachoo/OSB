__author__ = 'med'

import subprocess as sub
from app import app
import re
from flask import jsonify
import shlex
import operator
from swiftclient import client

auth_url = app.config['USER_AUTH_URL']


class User():
    """

    """

    @staticmethod
    def exists(user_name, user_pass):
        cmd = "swift list --os-tenant-name " + user_name + " --os-username " + user_name + " --os-password " \
              + user_pass + " --os-auth-url " + auth_url
        args = shlex.split(cmd)
        print 'DEBUG:  api.User.exists.args: ' + str(args)
        not_found = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[1]
        print 'DEBUG:  api.User.exists.args.not_found ' + not_found
        if not_found:
            print 'DEBUG: api.User.exists = False'
            return False
        else:
            'DEBUG: api.User.exists = True'
            return True

    @staticmethod
    def get_info(user_name, user_pass):
        cmd = "swift --os-tenant-name " + user_name + " --os-username " + user_name + " --os-password " \
              + user_pass + " --os-auth-url " + auth_url + " stat -v"
        args = shlex.split(cmd)
        print 'DEBUG:  api.User.get_info.args: ' + str(args)
        out = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        print 'DEBUG:  api.User.get_info.out: ' + str(out[0].split())
        if not out[1]:
            index = out[0].split().index('StorageURL:')
            index1 = out[0].split().index('Token:')
            index2 = out[0].split().index('Account:')
            index3 = out[0].split().index('Containers:')
            index4 = out[0].split().index('Objects:')
            index5 = out[0].split().index('Bytes:')
            index6 = out[0].split().index('Temp-Url-Key:')
            StorageURL = out[0].split()[index + 1]
            Token = out[0].split()[index1 + 1]
            Account = out[0].split()[index2 + 1]
            Containers = out[0].split()[index3 + 1]
            Objects = out[0].split()[index4 + 1]
            Bytes = out[0].split()[index5 + 1]
            TempURLkey = out[0].split()[index6 + 1]
            infos = {'StorageURL': StorageURL, 'Token': Token, 'Account': Account, 'Containers': Containers,
                     'Objects': Objects, 'Bytes': Bytes, 'Temp_Url_Key': TempURLkey}
            print 'DEBUG:  api.User.get_info.infos: ' + str(infos)
            return infos
        return False


class AddUser():
    """

    """

    @staticmethod
    def add_user(user_name, user_pass, user_email):
        admin_tenant = app.config['ADMIN_TENANT_NAME']
        admin_username = app.config['ADMIN_USERNAME']
        admin_pass = app.config['ADMIN_PASSWORD']
        admin_auth_url = app.config['ADMIN_AUTH_URL']
        cmd = "keystone --os-tenant-name " + admin_tenant + " --os-username " + admin_username + " --os-password " \
              + admin_pass + " --os-auth-url " + admin_auth_url + " tenant-create --name " + user_name \
              + " --description " + '"' + user_name + " Tenant" + '"'
        args = shlex.split(cmd)
        print 'DEBUG:  api.AddUser.add_user.args: ' + str(args)
        tenant_exists = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[1]
        if tenant_exists:
            print 'DEBUG:  api.AddUser.add_user.tenant_exists = TRue'
            return False
        else:
            print 'DEBUG:  api.AddUser.add_user.tenant_exists = True'
            cmd = "keystone --os-tenant-name " + admin_tenant + " --os-username " + admin_username + " --os-password " \
                  + admin_pass + " --os-auth-url " + admin_auth_url + " user-list"
            args = shlex.split(cmd)
            print 'DEBUG:  api.AddUser.add_user.args: ' + str(args)
            output = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
            print 'DEBUG:  api.AddUser.add_user.output: ' + str(output[0].split())
            emails_list = []
            if not output[1]:
                parsed = output[0].split()
                for i in range(0, len(parsed)):
                    bool = re.match("[^@]+@[^@]+\.[^@]+", parsed[i])
                    if bool:
                        emails_list.append(parsed[i])
                print 'DEBUG:  api.AddUser.add_user.emails_list: ' + str(emails_list)
                if user_email in emails_list:
                    print 'DEBUG:  api.AddUser.add_user(user_email in emails_list) = TRue'
                    return False
                else:
                    cmd = "keystone --os-tenant-name " + admin_tenant + " --os-username " + admin_username + " --os-password " \
                          + admin_pass + " --os-auth-url " + admin_auth_url + " user-create --name " + user_name + " --tenant " \
                          + user_name + " --pass " + user_pass + " --email " + user_email
                    args = shlex.split(cmd)
                    print 'DEBUG:  api.AddUser.add_user.args: ' + str(args)

                    user_exists = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[1]
                    if user_exists:
                        print 'DEBUG:  api.AddUser.add_user.user_exists = TRue'
                        return False
                    return True

    @staticmethod
    def gen_temp_url_key(user_name, user_pass):
        cmd = "openssl rand -hex 30"
        args = shlex.split(cmd)
        print 'DEBUG:  api.User.gen_temp_url_key.args: ' + str(args)
        out = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        print 'DEBUG:  api.User.gen_temp_url_key.out: ' + str(out[0].split())
        temp_key = out[0]
        if not out[1]:
            cmd = "swift --os-tenant-name " + user_name + " --os-username " + user_name + " --os-password " \
                  + user_pass + " --os-auth-url " + auth_url + " post -m Temp-Url-Key:" + temp_key
        args = shlex.split(cmd)
        print 'DEBUG:  api.User.gen_temp_url_key.args: ' + str(args)
        out = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        print 'DEBUG:  api.User.gen_temp_url_key.out: ' + str(out[0].split())
        print 'DEBUG:  api.User.gen_temp_url_key.err: ' + str(out[1].split())
        if not out[1]:
            return True
        return False


class Containers():
    """

    """

    @staticmethod
    def list(url, token):
        cmd = "curl -X GET -H 'X-Auth-Token: " + token + "' " + url + "/"
        args = shlex.split(cmd)
        print 'DEBUG: api.Containers.list().args: ' + str(args)
        cont_l = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
        cont_list = str(cont_l).split('\n')
        cont_list.sort()
        print 'DEBUG: api.Containers.list().type(cont_list): '+str(type(cont_list))
        print 'DEBUG: api.Containers.list().cont_list: ' + str(cont_list)
        # print 'DEBUG: api.Containers.list().cont_list[1]: '+str(cont_list[1])
        if cont_list:
            print cont_list
            print type(cont_list)
            if cont_list == '<html><h1>Unauthorized</h1><p>This server could not verify that you are authorized ' \
                                  'to access the document you requested.</p></html>':
                return cont_list
            l = cont_list
            cont_dict = {}
            for i in range(0, len(l)):
                #print str(i)+": "+l[i]
                #print i, str(i)
                cont_dict[str(i)] = l[i]
                #print cont_dict[str(i)]
            #print cont_dict

            # print jsonify(**cont_dict)
            return cont_dict
        else:
            return False

    @staticmethod
    def create(url, token, container_name):
        cmd = "curl -X PUT -H 'X-Auth-Token: " + token + "' " + url + "/" + container_name
        args = shlex.split(cmd)
        print 'DEBUG: api.Containers.create().args: ' + str(args)
        cont_create = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        print 'DEBUG: api.containers.create.stderr: ' + str(cont_create[1])
        print 'DEBUG: api.containers.create.stdout: ' + str(cont_create[0])
        if cont_create[1]:
            return True
        return False

    @staticmethod
    def delete(url, token, container_name):
        cmd = "curl -X DELETE -H 'X-Auth-Token: " + token + "' " + url + "/" + container_name
        args = shlex.split(cmd)
        print 'DEBUG: api.Containers.delete().args: ' + str(args)
        cont_delete = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        print 'DEBUG: api.containers.delete.stderr: ' + str(cont_delete[1])
        print 'DEBUG: api.containers.delete.stdout: ' + str(cont_delete[0])
        if cont_delete[1]:
            return True
        return False



class Objects():
    """

    """

    @staticmethod
    def list(url, token, container_name):
        try:
            container_meta_data, objects_list = client.get_container(url, token, container_name, delimiter='/')
        except client.ClientException:
            return False
        print container_name, objects_list
        for i in range(0, len(objects_list)):
            objects_list[i]['name'] = container_name+'/'+objects_list[i]['name'].decode('utf-8')
            objects_list[i]['bytes'] = objects_list[i]['bytes']/1024
            objects_list[i]['content_type'] = objects_list[i]['content_type'][12:]
            temp = objects_list[i]['last_modified'].split('T')
            objects_list[i]['last_modified'] = temp[0]+" "+temp[1][:8]
        return objects_list

        '''
        cmd = "curl -X GET -H 'X-Auth-Token: " + token + "' " + url + "/" + container_name
        args = shlex.split(cmd)
        print 'DEBUG: api.Objects.list().args: ' + str(args)
        objs_list = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        print 'DEBUG: api.Objects.list().stderr: ' + str(objs_list[1])
        print 'DEBUG: api.Objects.list().strout: ' + str(objs_list[0])

        if objs_list[0]:
            b = objs_list[0].split()
            objs_dict = {}
            for i in range(0, len(b)):
                objs_dict[str(i)] = container_name+'/'+b[i].decode('utf-8')
            print 'DEBUG: api.Objects.list().objs_dict: ' + str(objs_dict)
            if container_name+'/Found</h1><p>The' in objs_dict.values():
                objs_dict = {}
            print 'DEBUG: api.Objects.list().objs_dict: ' + str(objs_dict.values())
            #objs_dict_by_cont = {container_name: objs_dict}
            return objs_dict
        else:
            return False
        '''



    @staticmethod
    def upload(url, token, container_name, object_name):
        cmd = "curl -X PUT -T "+object_name+" -H 'X-Auth-Token: " + token + "' " + url + "/" + container_name + "/" + object_name
        args = shlex.split(cmd)
        print 'DEBUG: api.Objects.upload().args: ' + str(args)
        obj_up = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        print 'DEBUG: api.Objects.upload().stderr: ' + str(obj_up[1])
        print 'DEBUG: api.Objects.upload().strout: ' + str(obj_up[0])

        if not obj_up[1]:
            return True
        else:
            return False

    @staticmethod
    def delete(url, token, container_name, object_name):
        cmd = "curl -X DELETE  -H 'X-Auth-Token: " + token + "' " + url + "/" + container_name + "/" + object_name
        args = shlex.split(cmd)
        print 'DEBUG: api.DeleteObject.obj_del().args: ' + str(args)
        obj_del = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        print 'DEBUG: api.Objects.delete().stderr: ' + str(obj_del[1])
        print 'DEBUG: api.Objects.delete().strout: ' + str(obj_del[0])

        if obj_del[1]:
            return True
        else:
            return False

    @staticmethod
    def share(host, method, seconds, account, container, obj, key):
        s = "/v1/{account}/{container}/{obj}"
        path = s.format(account=account, container=container, obj=obj)
        cmd = sub.Popen(["swift-temp-url", method, seconds, path, key], stdout=sub.PIPE).communicate()[0]
        temp_url = host + cmd[:-1] + "&inline"
        return temp_url

    @staticmethod
    def download(host, method, seconds, account, container, obj, key):
        s = "/v1/{account}/{container}/{obj}"
        path = s.format(account=account, container=container, obj=obj)
        cmd = sub.Popen(["swift-temp-url", method, seconds, path, key], stdout=sub.PIPE).communicate()[0]
        temp_url = host + cmd[:-1]
        return temp_url

        '''
        cmd = "curl -X GET -H 'X-Auth-Token: " + token + "' " + url + "/" + container_name + "/" + object_name+" -O "+object_name  #!!!!
        args = shlex.split(cmd)
        print 'DEBUG: api.DownloadObject.download_object().args: ' + str(args)
        obj_down = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE, shell=True).communicate()
        print 'DEBUG: api.Objects.download().stderr: ' + str(obj_down[1])
        print 'DEBUG: api.Objects.download().strout: ' + str(obj_down[0])

        if not obj_down[1]:
            return True
        else:
            return False
        '''












