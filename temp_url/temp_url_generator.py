__author__ = 'med'

import subprocess as sub


class Container():
    """
    List_containers lists the account's containers
    """

    def __init__(self):
        pass

    def list_containers(self):
        """list the account's containers"""
        cont = sub.Popen(["swift", "list", "--os-username", "med", "--os-password", "med", "--os-tenant-name", "med",
                          "--os-auth-url", "http://controller:5000/v2.0"], stdout=sub.PIPE).communicate()[0].split()
        # print "> Your account contains the following containers: "
        dic = {}
        for i in range(0, len(cont)):
            dic.update({i: cont[i]})
            print str(i) + ": " + cont[i]
        return dic

    def chosen_container(self, dic):
        """choose a container from the listed ones"""
        var = int(raw_input("> Choose container: "))
        if var in dic:
            print "> You have chosen: " + dic[var]
            container = dic[var]
        else:
            print "ERROR: index out of bound"
            exit(1)
        return container

    def list_objects(self, container):
        objs = sub.Popen(
            ["swift", "list", container, "--os-username", "med", "--os-password", "med", "--os-tenant-name", "med",
             "--os-auth-url", "http://controller:5000/v2.0"], stdout=sub.PIPE).communicate()[0].split()
        return objs


class Generator():
    """
    Temp_url_gen generates temporary urls for a chosen container. Note that a container is an element of the swift
    object hierarchy via its access url; http://<host>:8080/v1/<account>/<container>/<object>

    Attributes:
        name : A string that represents the name of the container, the one you would like to generate temporary urls on
        its objects.
        method :  The method to allow; GET for example.
        seconds : The number of seconds from now to allow requests.

    """

    def __init__(self, container, method, seconds):
        """ Returns a temp_url_gen object that will generate temporary urls for the objects in the container *name*.
            Those temp_urls will allow only the method *method* for a duration of *seconds*"""
        self.container = container
        self.method = method
        self.seconds = seconds

    def get_data(self):
        """extract needed data from the command ; $ swift -v stat"""
        data = sub.Popen(
            ["swift", "-v", "stat", "--os-username", "med", "--os-password", "med", "--os-tenant-name", "med",
             "--os-auth-url", "http://controller:5000/v2.0"], stdout=sub.PIPE).communicate()[0].split()
        for i in range(0, len(data)):
            if data[i] == "StorageURL:":
                storage_url = data[i + 1]
                # print data[i]+storage_url
            if data[i] == "Account:":
                account = data[i + 1]
                # print data[i]+account
            if data[i] == "Token:":
                auth_token = data[i + 1]
                # print data[i]+auth_token
            if data[i] == "Temp-Url-Key:":
                key = data[i + 1]
                # print data[i]+key
        return storage_url, account, auth_token, key

    def get_host(self, storage_url, account):
        """extract the host url"""
        host = storage_url.strip(account).strip('/v1/')
        return host

    def generate(self, host, method, seconds, account, container, objs, key):
        """generate the temp_urls for the container objects"""
        for i in range(0, len(objs)):
            obj = objs[i]
            s = "/v1/{account}/{container}/{obj}"
            path = s.format(account=account, container=container, obj=obj)
            cmd = sub.Popen(["swift-temp-url", method, seconds, path, key], stdout=sub.PIPE).communicate()[0]
            temp_url = host + cmd[:-1] + "&inline"
            print objs[i]
            print temp_url
            print ""