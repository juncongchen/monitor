#!/usr/bin/env python
import inspect
import time
import urllib, urllib2
import json
import socket
from pollster import cpu,mem


def getTime():
    t = str(int(time.time()) + 8 * 3600)
    print 'time: ' + t
    return t


def getHost():
    host = socket.gethostname()
    print 'host: ' + host
    return host

if __name__ == "__main__":
    while True:
        t = getTime()
        host = getHost()
        cpuusage = cpu.getCPUUsage()
        memdata = mem.getMemData()
        # print data
        # req = urllib2.Request("http://51reboot.com:8888", json.dumps(data), {'Content-Type': 'application/json'})
        # f = urllib2.urlopen(req)
        # response = f.read()
        # print response
        # f.close()
        time.sleep(5)
