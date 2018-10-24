#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pika
import datetime
import json
import time
import MySQLdb


# 创建socket链接,声明管道
connect = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connect.channel()
# 声明exchange名字和类型
channel.exchange_declare(exchange="practice", exchange_type="fanout")

args = {'x-message-ttl':864000000, 'x-max-length-bytes': 5000000000}
result = channel.queue_declare(queue='monitor',durable=True,arguments=args)
queue_name = result.method.queue
print('当前queue名称：', queue_name)
# 绑定exchange, 相当于打开收音机，锁定了一个FM频道
channel.queue_bind(exchange="practice",
                   queue=queue_name)

today = datetime.datetime.now().strftime('%Y%m%d')

# 建立数据库连接，使用cursor()方法获取操作游标
db = MySQLdb.connect("localhost", "root", "123456", "monitor")
cursor = db.cursor()

sql = """INSERT  INTO t_%s (host_id,metric_id,time,value) VALUE ((SELECT id from t_host where name = %s), (SELECT id from t_metric where metric_name = %s), %s, %s)"""

# 将数据转化成sql语句的参数格式
def getargs(data) :
    # sql_arg = [('表名'，'host','metric','time','value')]
    # data = [{"cpu.iowait": 0.0, "cpu.stealstolen": 0.0, "mem.Cached": "231096", "cpu.guest": 0.0, "mem.MemFree": "359708", "mem.Buffers": "62344", "mem.Inactive": "207272", "cpu.system": 0.0, "cpu.user": 9.0899999999999999, "mem.Used": 350964, "cpu.irq": 0.0, "host": "host01", "mem.MemTotal": "1004112", "time": "20181024113928", "cpu.nice": 0.0, "cpu.idle": 90.909999999999997, "mem.Active": "263328", "cpu.softirq": 0.0}, {"cpu.iowait": 0.0, "mem.Cached": "231100", "cpu.guest": 0.0, "mem.Buffers": "62344", "mem.Inactive": "207280", "cpu.system": 0.0, "cpu.user": 27.27, "mem.Used": 351040, "cpu.irq": 0.0, "host": "host01", "mem.MemTotal": "1004112", "cpu.idle": 72.730000000000004, "cpu.nice": 0.0, "time": "20181024113929", "mem.Active": "263404", "mem.MemFree": "359628", "cpu.stealstolen": 0.0, "cpu.softirq": 0.0}, {"cpu.iowait": 0.0, "cpu.stealstolen": 0.0, "mem.Cached": "231100", "cpu.guest": 0.0, "mem.Buffers": "62344", "mem.Inactive": "207280", "cpu.system": 9.0899999999999999, "cpu.user": 18.18, "mem.Used": 351132, "cpu.irq": 0.0, "host": "host01", "mem.MemTotal": "1004112", "time": "20181024113930", "cpu.nice": 0.0, "mem.MemFree": "359536", "mem.Active": "263432", "cpu.softirq": 0.0, "cpu.idle": 72.730000000000004}, {"cpu.iowait": 0.0, "mem.Cached": "231104", "cpu.guest": 0.0, "mem.MemFree": "359660", "mem.Buffers": "62352", "cpu.nice": 0.0, "mem.Inactive": "207284", "cpu.system": 0.0, "cpu.user": 10.0, "mem.Used": 350996, "cpu.irq": 0.0, "host": "host01", "mem.MemTotal": "1004112", "time": "20181024113939", "mem.Active": "263384", "cpu.idle": 90.0, "cpu.stealstolen": 0.0, "cpu.softirq": 0.0}]
    sql_arg = []
    for d in data:
        host = d.pop('host')
        time = d.pop('time')
        table = int(str(time)[0:10])
        for key in d:
            sql_arg.append((table, host, key, time, d[key]))
    # print(sql_arg)
    return sql_arg

# 回调函数
def callback(ch, method, properties, body):
    start = time.time()
    data = str("{0}".format(body)).strip( 'b\'' )
    # print(data)
    sql_arg = getargs(json.loads(data))
    try:
        # 执行SQL语句
        cursor.executemany(sql,sql_arg)
        db.commit()
    except Exception as e:
        print(e)
        print("Error: unable to fetch data")
    print('用时：', time.time() - start)


# 消费信息
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

# 开始消费
channel.start_consuming()






