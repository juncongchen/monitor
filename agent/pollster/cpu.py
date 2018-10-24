#!/usr/bin/env python
import time
from collections import OrderedDict


def read_proc_stat():
    cpu_line = OrderedDict()
    with open('/proc/stat') as f:
        lines = f.readlines()
        line = lines[0]
        tmp = line.strip().split()
        cpu_line = tmp[1:len(tmp)]
        # print cpu_line
    return cpu_line


def getCPUUsage():
    cpu_usage = {}
    cpu_line = read_proc_stat()
    total_1 = {}
    idle_1 = {}
    total_2 = {}
    idle_2 = {}

    if cpu_line:
        total_1 = float(cpu_line[0]) + float(cpu_line[1]) + \
                        float(cpu_line[2]) + float(cpu_line[3]) + \
                        float(cpu_line[4]) + float(cpu_line[5]) + float(cpu_line[6]) + \
                        float(cpu_line[7]) + float(cpu_line[8])

        time.sleep(0.1)

        cpu_line_2 = read_proc_stat()

        index = ['user', 'nice' , 'system' ,'idle' ,'iowait' , 'irq' , 'softirq' , 'stealstolen'  ,  'guest']

        if cpu_line_2:
            total_2 = float(cpu_line_2[0]) + float(cpu_line_2[1]) + \
                      float(cpu_line_2[2]) + float(cpu_line_2[3]) + \
                      float(cpu_line_2[4]) + float(cpu_line_2[5]) + float(cpu_line_2[6]) + \
                      float(cpu_line_2[7]) + float(cpu_line_2[8])

        if total_1 and total_2:
            for i in range(len(index)):
		cpu_usage['cpu.'+index[i]] = round(100 * ((float(cpu_line_2[i]) - float(cpu_line[i])) / float(total_2 - total_1)), 2)
    print 'cpu_usage: ' + str(cpu_usage)
    return cpu_usage