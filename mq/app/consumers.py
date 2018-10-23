#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pika
import datetime
import json
import time
# import fcntl
from app import storage2

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

# 回调函数
def callback(ch, method, properties, body):
    start = time.time()
    data = str("{0}".format(body)).strip( 'b\'' )
    with open('./cache.txt', 'r+') as f:
        # fcntl.flock(f, fcntl.LOCK_EX)   # 为了避免同时操作文件，对文件进行加锁。这里如果检查到已经加锁了，进程会被阻塞
        cache = json.loads(f.read())
        cache.extend(json.loads(data))
        f.seek(0)
        f.truncate()
        f.write(json.dumps(cache))
        f.close()
    print(time.time() - start)


# 消费信息
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
# 开始消费
channel.start_consuming()

