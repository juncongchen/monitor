#!/usr/bin/env python#!/usr/bin/python
import inspect
import time
import datetime
import urllib, urllib2
import json
import socket
import fcntl
from pollster import cpu,mem


def getTime():
    t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
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
	data = {'host':host,'time':t}
	data.update(cpudata)
	data.update(memdata)
	with open('./cache') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            cache = json.loads(f.read())
            print cache
        cache.append(data)
	textmod = json.dumps(cache)
        print textmod
	try:
	    url='http://10.1.177.35:5000/post'
	    req = urllib2.Request(url,textmod,{'Content-Type': 'application/json'})
	    res = urllib2.urlopen(req,timeout = 0.1)
        except urllib2.URLError, e:
            try :
                print 'retransmission'
                res = urllib2.urlopen(req,timeout = 0.1)
            except Exception,e :
                print e
        except Exception,e :
            print e
	else :
            cache = []
            res = res.read()
	    print(res)
        with open('./cache','w+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(json.dumps(cache))
            f.close()

        time.sleep(59)
