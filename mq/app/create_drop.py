#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 每天执行一次，创建明天的表，删除7天前的表

import datetime
import MySQLdb

now = datetime.datetime.now()

# 建表语句
create_sql = """CREATE TABLE IF NOT EXISTS t_%d (
              `host_id` int(32) NOT NULL,
              `metric_id` int(32) NOT NULL,
              `time` bigint(32) NULL,
              `value` bigint(32) NULL,
              INDEX `time_host`(`time`, `host_id`)
            ) ENGINE = InnoDB;"""
delta = datetime.timedelta(days=1)
tomorrow = int((now + delta).strftime('%Y%m%d')+'00')
create_list = [(tomorrow)]
hour = 1
while hour < 24:
    create_list.append((tomorrow+hour))
    hour+=1
print(create_list)

# 删表语句
drop_sql = """DROP TABLE IF EXISTS  t_%d """
delta = datetime.timedelta(days=7)
dropdate = int((now - delta).strftime('%Y%m%d')+'00')
drop_list=[dropdate]
hour = 1
while hour < 24:
    drop_list.append((dropdate+hour))
    hour+=1
print(drop_list)

# 建立数据库连接，使用cursor()方法获取操作游标
db = MySQLdb.connect("localhost", "root", "123456", "monitor")
cursor = db.cursor()

try:
    # cursor.executemany(query=create_sql,args=times)
    for item in create_list:
        cursor.execute(create_sql %item)
        cursor.execute(drop_sql %drop_list[create_list.index(item)])
    db.commit()
except Exception as e:
    print(e)
    print("Error: unable to fetch data")

# 关闭数据库连接
db.close()