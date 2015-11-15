__author__ = 'med'

import subprocess
import psutil


class PerfCheck():
    def __init__(self):
        pass

    def check_cpu(self):
        return psutil.cpu_percent(interval=1, percpu=True)

    def check_ram(self):
        return psutil.used_phymem

    def check_swp(self):
        return psutil.swap_memory()

##############################
while True:
    perf = PerfCheck()
    cpu = perf.check_cpu()
    mem = perf.check_ram()
    swp = perf.check_swp()
    print cpu, mem, swp

'''
import shlex
cmd = "top -b -n 1"  # or whatever you use
args = shlex.split(cmd)
print args
output = subprocess.Popen(["top","-b", "-n", "1"], stdout=subprocess.PIPE).communicate()[0].split('\n')[2]
cpuline = output
print cpuline
'''