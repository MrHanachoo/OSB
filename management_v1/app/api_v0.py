__author__ = 'med'

import subprocess as sub
from app import app
import re
from flask import jsonify


class User():
    """

    """
    auth_url = app.config['USER_AUTH_URL']

    def __init__(self, user_name, user_pass):
        self.user_name = user_name
        self.user_pass = user_pass


    def exists(self):
        not_found = sub.Popen(
            ["swift", "list", "--os-tenant-name", self.user_name, "--os-username", self.user_name, "--os-password",
             self.user_pass, "--os-auth-url", self.auth_url], stdout=sub.PIPE, stderr=sub.PIPE).communicate()[1]
        if not_found:
            return False
        else:
            return True

    def get_ids(self):
        out = sub.Popen(
            ["keystone", "--os-tenant-name", self.user_name, "--os-username", self.user_name, "--os-password",
             self.user_pass, "--os-auth-url", self.auth_url, "token-get"], stdout=sub.PIPE,
            stderr=sub.PIPE).communicate()
        if not out[1]:
            index = out[0].split().index('tenant_id')
            index1 = out[0].split().index('user_id')
            tenant_id = out[0].split()[index + 2]
            user_id = out[0].split()[index1 + 2]
            ids = {'tenant_id': tenant_id, 'user_id': user_id}
            return ids
        return False


class AddUser():
    """

    """

    def __init__(self, user_name, user_pass, user_email):
        self.user_name = user_name
        self.user_pass = user_pass
        self.user_email = user_email

    def add_user(self):
        admin_tenant = app.config['ADMIN_TENANT_NAME']
        admin_username = app.config['ADMIN_USERNAME']
        admin_pass = app.config['ADMIN_PASSWORD']
        admin_auth_url = app.config['ADMIN_AUTH_URL']
        tenant_exists = sub.Popen(["keystone", "--os-tenant-name", admin_tenant, "--os-username", admin_username,
                                   "--os-password", admin_pass, "--os-auth-url", admin_auth_url,
                                   "tenant-create", "--name", self.user_name, "--description",
                                   self.user_name + " Tenant"],
                                  stdout=sub.PIPE, stderr=sub.PIPE).communicate()[1]
        if tenant_exists:
            return False
        else:
            output = sub.Popen(
                ["keystone", "--os-tenant-name", admin_tenant, "--os-username", admin_username, "--os-password",
                 admin_pass, "--os-auth-url", admin_auth_url, "user-list"], stdout=sub.PIPE,
                stderr=sub.PIPE).communicate()
            emails_list = []
            if not output[1]:
                parsed = output[0].split()
                for i in range(0, len(parsed)):
                    bool = re.match("[^@]+@[^@]+\.[^@]+", parsed[i])
                    if bool:
                        emails_list.append(parsed[i])
                print emails_list
                if self.user_email in emails_list:
                    return False
                else:
                    user_exists = \
                        sub.Popen(["keystone", "--os-tenant-name", admin_tenant, "--os-username", admin_username,
                                   "--os-password", admin_pass, "--os-auth-url", admin_auth_url,
                                   "user-create", "--name", self.user_name, "--tenant", self.user_name, "--pass",
                                   self.user_pass,
                                   "--email", self.user_email], stdout=sub.PIPE, stderr=sub.PIPE).communicate()[1]
                    if user_exists:
                        return False
                    return True


class Containers():
    """

    """

    def __init__(self, user_name, user_pass):
        self.username = user_name
        self.passwd = user_pass

    @staticmethod
    def list(self):
        user_auth_url = app.config['USER_AUTH_URL']
        cont_list = sub.Popen(["swift", "list", "--os-tenant-name", self.username, "--os-username", self.username,
                               "--os-password", self.passwd, "--os-auth-url", user_auth_url],
                              stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        if not cont_list[1]:
            return jsonify(cont_list[0].split())
        else:
            return False


class Objects():
    """

    """

    def __init__(self, username, passwd, container):
        self.username = username
        self.passwd = passwd
        self.container = container

    def list(self):
        user_auth_url = app.config['USER_AUTH_URL']
        obj_list = sub.Popen(
            ["swift", "list", self.container, "--os-tenant-name", self.username, "--os-username", self.username,
             "--os-password", self.passwd, "--os-auth-url", user_auth_url],
            stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        if not obj_list[1]:
            return obj_list[0].split()
        else:
            return False


class Upload():
    """

    """

    def __init__(self, username, passwd, container, file_path):
        self.username = username
        self.passwd = passwd
        self.container = container
        self.file_path = file_path

    def upload(self):
        user_auth_url = app.config['USER_AUTH_URL']
        upload = sub.Popen(
            ["swift", "upload", self.container, self.file_path, "--os-tenant-name", self.username, "--os-username",
             self.username,
             "--os-password", self.passwd, "--os-auth-url", user_auth_url],
            stdout=sub.PIPE, stderr=sub.PIPE, shell=True).communicate()
        if not upload[1]:
            return True
        else:
            return False


class DownloadObject():
    """

    """

    def __init__(self):
        pass

    def download_object(self, username, passwd, container, object):
        user_auth_url = app.config['USER_AUTH_URL']
        download_obj = sub.Popen(
            ["swift", "download", container, object, "--os-tenant-name", username, "--os-username", username,
             "--os-password", passwd, "--os-auth-url", user_auth_url],
            stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        if not download_obj[1]:
            return True
        else:
            return False


class DownloadContainer():
    """

    """

    def __init__(self):
        pass

    def download_container(self, username, passwd, container):
        user_auth_url = app.config['USER_AUTH_URL']
        download_all = sub.Popen(
            ["swift", "download", container, "--os-tenant-name", username, "--os-username", username,
             "--os-password", passwd, "--os-auth-url", user_auth_url],
            stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        if not download_all[1]:
            return True
        else:
            return False


class DownloadAll():
    """

    """

    def __init__(self):
        pass

    def download_all(self, username, passwd):
        user_auth_url = app.config['USER_AUTH_URL']
        download_all = sub.Popen(["swift", "download", "--os-tenant-name", username, "--os-username", username,
                                  "--os-password", passwd, "--os-auth-url", user_auth_url],
                                 stdout=sub.PIPE, stderr=sub.PIPE).communicate()
        if not download_all[1]:
            return True
        else:
            return False

