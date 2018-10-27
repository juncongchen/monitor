#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pika
from flask import request
from app import app

# 创建socket实例，声明管道
# credentials = pika.PlainCredentials('mx', 'zaq1@WSXcde3')
# connect = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
connect = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connect.channel()

print("build")

# 声明exchange、queue的名字和类型
channel.exchange_declare(exchange="practice",
                         exchange_type="fanout")

# x-message-ttl:队列中消息的保存时间，单位ms
# x-max-length-bytes：队列的最大容量，单位B
# x-max-length ： 队列可容纳最大消息数，单位条
args = {'x-message-ttl': 864000000, 'x-max-length-bytes': 5000000000}
channel.queue_declare(queue='monitor', durable=True, arguments=args)

@app.route("/post", methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        data = request.data
    else:
        data = request.args.get("data")

    # 广播一个消息
    channel.basic_publish(
        exchange="practice",
        routing_key='',
        body=data,
        properties=pika.BasicProperties(
            delivery_mode = 2,          # 持久化
        )
    )
    print(data)

    return "success"
