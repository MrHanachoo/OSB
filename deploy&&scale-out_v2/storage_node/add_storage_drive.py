__author__ = 'med'

import subprocess as sub


class AddStorageDrive():
    def __init__(self):
        pass

    def plug(self, device_name):
        sub.call(["chmod", "u+x", "bin/plug.sh"])
        sub.call(["bin/plug.sh", device_name])

