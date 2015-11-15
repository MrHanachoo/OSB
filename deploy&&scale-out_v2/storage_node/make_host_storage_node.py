__author__ = 'med'

import subprocess as sub


class MakeHostStorageNode():
    def __init__(self):
        pass

    def deploy(self):
        sub.call(["chmod", "u+x", "bin/make_host_storage_node.sh"])
        sub.call(["bin/make_host_storage_node.sh"])
