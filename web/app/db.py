#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import MySQLdb
import datetime
from app import app
from flask import request

# 建立数据库连接，使用cursor()方法获取操作游标
db = MySQLdb.connect("localhost", "root", "123456", "monitor")
cursor = db.cursor()

@app.route('/query', methods=['GET', 'POST'])
def getdata():
    if request.method == 'POST':
        host = request.form["host"]
        range = request.form["time"]
        metric = request.form["metric"]
    else:
        host = request.args.get("host")
        range = request.args.get("time")
        metric = request.args.get("metric")
    print(host,metric,range)
    return query(host,metric,range)

def query(host,metric,range):
    now = datetime.datetime.now()
    table = []
    if range==None or len(range)==0:
        range=1

    i = int(range)-1
    while i >= 0:
        headhour = int((now-datetime.timedelta(hours=i)).strftime('%Y%m%d%H'))
        table.append(headhour)
        i-=1
    last_table = int((now-datetime.timedelta(hours=int(range))).strftime('%Y%m%d%H'))
    minute = now.strftime('%M')
    # print(table,last_table,minute)

    if host == None or len(host) == 0:
        host = 'host01'
    if metric == None or len(metric) == 0:
        metric = "cpu"

    sql = """SELECT b.name, c.metric_name, a.time ,a.value, a.unit FROM t_%%d AS a
            INNER JOIN t_host AS b ON	a.host_id = b.id AND b.name = "%s"
            INNER JOIN t_metric AS c ON a.metric_id = c.id AND c.metric_name LIKE "%s%%%%" 
            ORDER BY a.time;""" %(host,metric)

    last_sql = """SELECT b.name, c.metric_name, a.time ,a.value, a.unit FROM t_%d AS a
                INNER JOIN t_host AS b ON	a.host_id = b.id AND b.name = "%s" AND a.time >= %s
                INNER JOIN t_metric AS c ON a.metric_id = c.id AND c.metric_name LIKE "%s%%" 
                ORDER BY a.time;""" %(last_table,host,minute,metric)

    # print(sql,last_sql)

    data = {}
    try:
        # 执行SQL语句
        cursor.execute(last_sql)
        data[str(last_table)] = cursor.fetchall()
        for item in table:
            # print(sql %item)
            cursor.execute(sql %item)
            data[str(item)]=cursor.fetchall()
        db.commit()
        # print(data)

        unit = ''
        metriclist = []
        time = []
        value = {}
        for key in data:
            if len(data[key])==0:
                continue
            for item in data[key]:
                unit = item[4]
                z=str(item[1]).split('.')[1]
                t=key+ ((str(item[2])) if len(str(item[2]))==2 else '0'+str(item[2]))
                if metriclist.count(z) ==0 :
                    metriclist.append(z)
                    value[z]=[]
                if time.count(t) ==0 :
                    time.append(t)
            print(time, metriclist)

            for item in data[key]:
                value[str(item[1]).split('.')[1]].append(item[3])
            # print(value)

        data = {'title':host+'-'+metric,'time':time,'legend':metriclist,'value':value,'unit':'单位：'+unit}
        # print(data)

    except Exception as e:
        print(e)
        print("Error: unable to fetch data")

    return json.dumps(data)

if __name__ == "__main__":
    query('host01','cpu','1')
