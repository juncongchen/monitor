#!/usr/bin/env python

def getMemData():
    data = {
        'MemTotal' : getMemTotal(),
        'MemUsage' : getMemUsage(),
        'MemFree' : getMemFree()
    }
    print 'MemData:'+ str(data)
    return data

def getMemTotal():
    with open('/proc/meminfo') as mem_open:
        a = int(mem_open.readline().split()[1])
    return a / 1024


def getMemUsage(noBufferCache=True):
    if noBufferCache:
        with open('/proc/meminfo') as mem_open:
            T = int(mem_open.readline().split()[1])
            F = int(mem_open.readline().split()[1])
            B = int(mem_open.readline().split()[1])
            C = int(mem_open.readline().split()[1])
        return (T - F - B - C) / 1024
    else:
        with open('/proc/meminfo') as mem_open:
            a = int(mem_open.readline().split()[1]) - int(mem_open.readline().split()[1])
        return a / 1024


def getMemFree(noBufferCache=True):
    if noBufferCache:
        with open('/proc/meminfo') as mem_open:
            T = int(mem_open.readline().split()[1])
            F = int(mem_open.readline().split()[1])
            B = int(mem_open.readline().split()[1])
            C = int(mem_open.readline().split()[1])
        return (F + B + C) / 1024
    else:
        with open('/proc/meminfo') as mem_open:
            mem_open.readline()
            a = int(mem_open.readline().split()[1])
        return a / 1024
