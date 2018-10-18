#!/usr/bin/env python
import time
from collections import OrderedDict


def read_proc_stat():
    cpu_line = OrderedDict()
    with open('/proc/stat') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('cpu'):
                tmp = line.strip().split()
                cpu_line[tmp[0]] = tmp[1:len(tmp)]
    return cpu_line


def getCPUUsage():
    cpu_usage = {}
    cpu_line = read_proc_stat()
    total_1 = {}
    idle_1 = {}
    total_2 = {}
    idle_2 = {}

    if cpu_line:
        for item in cpu_line:
            total_1[item] = float(cpu_line[item][0]) + float(cpu_line[item][1]) + \
                            float(cpu_line[item][2]) + float(cpu_line[item][3]) + \
                            float(cpu_line[item][4]) + float(cpu_line[item][5]) + float(cpu_line[item][6])
            idle_1[item] = float(cpu_line[item][3])

        time.sleep(1)

        cpu_line_2 = read_proc_stat()

        if cpu_line_2:
            for item in cpu_line_2:
                total_2[item] = float(cpu_line_2[item][0]) + float(cpu_line_2[item][1]) + \
                                float(cpu_line_2[item][2]) + float(cpu_line_2[item][3]) + \
                                float(cpu_line_2[item][4]) + float(cpu_line_2[item][5]) + float(cpu_line_2[item][6])
                idle_2[item] = float(cpu_line_2[item][3])

        if total_1 and total_2:
            for item in total_1:
                cpu_usage[item] = {'volume': round(
                    100 * (1 - float(idle_2[item] - idle_1[item]) / float(total_2[item] - total_1[item])), 2),
                    'unit': '%'}
    print 'cpu_usage: ' + str(cpu_usage)
    return cpu_usage