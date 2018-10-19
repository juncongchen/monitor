#!/usr/bin/env python


def getMemData():
    mem_info = {}
    mem_data = {}
    index = ['MemTotal','MemFree','Buffers','Cached','Active','Inactive']

    try:
        with open('/proc/meminfo') as f:
            for line in f:
                tmp = line.split(':')
                if len(tmp) == 2:
                    vol_unit = tmp[1].strip().split(' ')
                    mem_info[tmp[0].strip()] = vol_unit[0]
    except:
        print "Unexpected error:", sys.exc_info()[1]
    finally:
        for item in index:
            mem_data[item] = mem_info[item]
        mem_data['used'] = mem_data['MemTotal'] - mem_data['MemFree'] - mem_data['Buffers'] - mem_data['Cached']
        print 'memdata: ' + mem_data
        return mem_data