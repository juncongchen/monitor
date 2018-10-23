#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import datetime
import time
import MySQLdb
# import fcntl

def receive(drop=False, data=[]):

    data = json.loads(data)
    start = time.time()
    # 按日期批量插入
    while len(data)>0 :
        temp = data.pop(0)
        Date = str(temp['time'])[0:8]
        datalist = [temp]
        data_copy = data
        data = []
        for item in data_copy :
            if str(item['time'])[0:8] == Date :
                datalist.append(item)
            else:
                data.append(item)
        storage(drop, datalist)
        print(time.time() - start)
        drop = False



def storage(drop, datalist) :
    t_cpu = 't_cpu_' + str(datalist[0]['time'])[0:8]
    t_mem = 't_mem_' + str(datalist[0]['time'])[0:8]
    cpu_column = "time, host_id, user, nice , system ,idle, iowait , irq , softirq , stealstolen "
    mem_column = "time, host_id, MemTotal,Used, MemFree,Buffers,Cached,Active,Inactive"

    # 建表语句
    create_cpu_sql = """CREATE TABLE IF NOT EXISTS %s (  
                          `time` bigint(32) NOT NULL,          
                          `host_id` int(32) NOT NULL,
                          `user` int(32) NULL,
                          `nice` int(32) NULL,
                          `system` int(32) NULL,
                          `idle` int(32) NULL,
                          `iowait` int(32) NULL,
                          `irq` int(32) NULL,
                          `softirq` int(32) NULL,
                          `stealstolen` int(32) NULL,
                          INDEX `index`(`time`, `host_id`)
                        ) ENGINE = InnoDB ;
                """ % t_cpu
    create_mem_sql = """CREATE TABLE IF NOT EXISTS %s (  
                              `time` bigint(32) NOT NULL,          
                              `host_id` int(32) NOT NULL,
                              `MemTotal` int(32) NOT NULL,          
                              `Used` int(32) NOT NULL,
                              `MemFree` int(32) NULL,
                              `Buffers` int(32) NULL,
                              `Cached` int(32) NULL,
                              `Active` int(32) NULL,
                              `Inactive` int(32) NULL,
                              INDEX `index`(`time`, `host_id`)
                            ) ENGINE = InnoDB ;
                    """ % t_mem

    # 插入语句
    inster_cpu_sql = "INSERT  INTO %s (%s) VALUE " % (t_cpu, cpu_column)
    inster_mem_sql = "INSERT  INTO %s (%s) VALUE " % (t_mem, mem_column)

    first = True
    for item in datalist:
        time = item['time']
        host = item['host']
        cpuData = item['cpudata']
        memData = item['memdata']
        if first:
            first = False
            inster_cpu_sql += "(%s, (SELECT id from t_host where name = \"%s\"), " % (time, host)
            inster_mem_sql += "(%s, (SELECT id from t_host where name = \"%s\"), " % (time, host)
        else:
            inster_cpu_sql += ",(%s, (SELECT id from t_host where name = \"%s\"), " % (time, host)
            inster_mem_sql += ",(%s, (SELECT id from t_host where name = \"%s\"), " % (time, host)
        inster_cpu_sql += "%(user)s, %(nice)s, %(system)s, %(idle)s, %(iowait)s, %(irq)s, %(softirq)s, %(stealstolen)s ) " %cpuData
        inster_mem_sql += " %(MemTotal)s, %(Used)s, %(MemFree)s, %(Buffers)s, %(Cached)s, %(Active)s, %(Inactive)s)" % memData

        # 删表语句
        if drop:
            today = datetime.datetime.now()
            delta = datetime.timedelta(days=7)
            before = today - delta
            drop_cpu_sql = """DROP TABLE IF EXISTS  %s""" % 't_cpu_' + before.strftime('%Y%m%d')
            drop_mem_sql = """DROP TABLE IF EXISTS  %s""" % 't_mem_' + before.strftime('%Y%m%d')

    # 建立数据库连接，使用cursor()方法获取操作游标
    db = MySQLdb.connect("localhost", "root", "123456", "monitor")
    cursor = db.cursor()

    try:
        # 执行SQL语句
        if drop:
            print('drop table')
            cursor.execute(drop_cpu_sql)
            cursor.execute(drop_mem_sql)
        cursor.execute(create_cpu_sql)
        cursor.execute(inster_cpu_sql)
        cursor.execute(create_mem_sql)
        cursor.execute(inster_mem_sql)
        db.commit()
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()



if __name__ == "__main__":
    today = datetime.datetime.now().strftime('%Y%m%d')
    while True :
        drop = False
        if today != datetime.datetime.now().strftime('%Y%m%d') :  # 判断是否需要删除过期的表格
            drop =True
            today = datetime.datetime.now().strftime('%Y%m%d')
        with open('./cache.txt','r+') as f:
            # fcntl.flock(f, fcntl.LOCK_EX)  # 为了避免同时操作文件，对文件进行加锁。这里如果检查到已经加锁了，进程会被阻塞
            data = f.read()
            try:
                receive(drop, data)
            except Exception as e :
                print(e)
            else:
                data = []
            f.seek(0)
            f.truncate()
            f.write(json.dumps(data))
            f.close()
        time.sleep(30)      # 定期连接数据库