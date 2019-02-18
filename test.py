#!/usr/bin/env python
import pika
import json

credentials = pika.PlainCredentials('root', 'root')
parameters = pika.ConnectionParameters('192.162.2.71',5673,'/',credentials)

connection = pika.BlockingConnection()
channel = connection.channel()

QUEUE_NAME = 'queue'
channel.queue_declare(queue=QUEUE_NAME)

def callback(ch, method, properties, body):
    data = json.loads(body)
    # name = data['name']
    # language = data['language']

    # print('Name: {}'.format(data['name']))      
    # print('Language: {}'.format(data['language']))
    
    print(" [x] Received %r" % body)

channel.basic_consume(callback, queue=QUEUE_NAME, no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

