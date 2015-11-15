__author__ = 'med'

import subprocess as sub


class ChangeControllerConfig():
    def __init__(self):
        pass

    def modify(self):
        sub.call(["chmod", "u+x", "bin/change_controller_node_ip_config_files.sh"])
        sub.call(["bin/change_controller_node_ip_config_files.sh"])






