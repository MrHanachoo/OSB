__author__ = 'med'

import os
import pprint
import subprocess


command = ['bash', '-c', 'source ~/demo-openrc.sh && env']

proc = subprocess.Popen(command, stdout=subprocess.PIPE)

for line in proc.stdout:
    (key, _, value) = line.partition("=")
    os.environ[key] = value

proc.communicate()

pprint.pprint(dict(os.environ))