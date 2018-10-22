#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pika
from app import storage

# 创建socket链接,声明管道
connect = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connect.channel()
# 声明exchange名字和类型
channel.exchange_declare(exchange="practice", exchange_type="fanout")
# rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除，result是queue的对象实例
args = {'x-message-ttl':3000000, 'x-max-length-bytes': 102400}
result = channel.queue_declare(queue='monitor',durable=True,arguments=args)
queue_name = result.method.queue
print('当前queue名称：', queue_name)
# 绑定exchange, 相当于打开收音机，锁定了一个FM频道
channel.queue_bind(exchange="practice",
                   queue=queue_name)


# 回调函数
def callback(ch, method, properties, body):
    data = str("{0}".format(body)).strip( 'b\'' )
    storage.receive(data)
    print(data)


# 消费信息
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
# 开始消费
channel.start_consuming()

