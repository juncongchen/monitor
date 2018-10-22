#!/usr/bin/env python#!/usr/bin/python
# -*- coding: UTF-8 -*-
import inspect
import time
import datetime
import urllib, urllib2
import json
import socket
from pollster import cpu,mem


def getTime():
    t = datetime.datetime.now().strftime('%Y%m%d%H%M')
    print 'time: ' + t
    return t


def getHost():
    host = socket.gethostname()
    print 'host: ' + host
    return host

if __name__ == "__main__":
    cache = []
    while True:
        t = getTime()
        host = getHost()
        cpudata = cpu.getCPUUsage()
        memdata = mem.getMemData()
        cache.append({'time':t,'host':host,'cpudata':cpudata,'memdata':memdata})
	textmod = json.dumps(cache)
        print textmod
	try:
	    url='http://192.168.1.206:5000/post'
	    req = urllib2.Request(url,textmod,{'Content-Type': 'application/json'})
	    res = urllib2.urlopen(req,timeout = 0.1)
        except urllib2.URLError, e:
            try :
                print 'retransmission'
                res = urllib2.urlopen(req,timeout = 1)
            except Exception,e :
                print e
        except Exception,e :
            print e
	else :
            cache = []
            res = res.read()
	    print(res)

        time.sleep(59)
