#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import pymysql

def receive(data):
    data = json.loads(data)

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
        storage(Date,datalist)


def storage(datalist) :
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

    # 建立数据库连接，使用cursor()方法获取操作游标
    db = pymysql.connect("localhost", "root", "123456", "monitor")
    cursor = db.cursor()

    try:
        # 执行SQL语句
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
    data = [{"cpudata": {"softirq": 0.0, "iowait": 0.0, "system": 0.0, "guest": 0.0, "idle": 100.0, "stealstolen": 0.0, "user": 0.0, "irq": 0.0, "nice": 0.0}, "host": "host01", "memdata": {"MemTotal": "1004112", "Cached": "506092", "MemFree": "96440", "Inactive": "286596", "Active": "438600", "Used": 356584, "Buffers": "44996"}, "time": "201810220001"},
            {"cpudata": {"softirq": 0.0, "iowait": 0.0, "system": 1.01, "guest": 0.0, "idle": 98.989999999999995, "stealstolen": 0.0, "user": 0.0, "irq": 0.0, "nice": 0.0}, "host": "host01", "memdata": {"MemTotal": "1004112", "Cached": "506092", "MemFree": "96440", "Inactive": "286604", "Active": "438612", "Used": 356576, "Buffers": "45004"}, "time": "201810220002"},
            {"cpudata": {"softirq": 0.0, "iowait": 0.0, "system": 0.0, "guest": 0.0, "idle": 100.0, "stealstolen": 0.0, "user": 0.0, "irq": 0.0, "nice": 0.0}, "host": "host01", "memdata": {"MemTotal": "1004112", "Cached": "506092", "MemFree": "96440", "Inactive": "286604", "Active": "438620", "Used": 356576, "Buffers": "45004"}, "time": "201810220003"},
            {"cpudata": {"softirq": 0.0, "iowait": 0.0, "system": 1.0, "guest": 0.0, "idle": 99.0, "stealstolen": 0.0, "user": 0.0, "irq": 0.0, "nice": 0.0}, "host": "host01", "memdata": {"MemTotal": "1004112", "Cached": "506092", "MemFree": "96440", "Inactive": "286612", "Active": "438628", "Used": 356568, "Buffers": "45012"}, "time": "201810230004"},
            {"cpudata": {"softirq": 0.0, "iowait": 0.0, "system": 0.0, "guest": 0.0, "idle": 100.0, "stealstolen": 0.0, "user": 0.0, "irq": 0.0, "nice": 0.0}, "host": "host01", "memdata": {"MemTotal": "1004112", "Cached": "506096", "MemFree": "96440", "Inactive": "286612", "Active": "438640", "Used": 356564, "Buffers": "45012"}, "time": "201810230005"}]

    receive(data)