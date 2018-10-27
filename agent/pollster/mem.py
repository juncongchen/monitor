#!/usr/bin/env python


def getMemData():
    mem_info = {}
    mem_data = {}
    unit = "KB"
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
            mem_data['mem.'+item] = {'value':mem_info[item],'unit':unit}
        mem_data['mem.Used'] = {'value':int(mem_info['MemTotal']) - int(mem_info['MemFree']) - int(mem_info['Buffers']) - int(mem_info['Cached']), 'unit':unit}
        print 'memdata: ' + str(mem_data)
        return mem_data
