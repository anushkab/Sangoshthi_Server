import pika
import json
import yaml


SERVER_TO_BROADCASTER = "server_to_broadcaster_ivr_9716517818"

credentials_b_s = pika.PlainCredentials('sangoshthi', 'sangoshthi')
parameters_b_s = pika.ConnectionParameters('192.168.2.71',5672,'/',credentials_b_s)

# broadcaster to server
connection_b_s = pika.BlockingConnection()
channel_b_s = connection_b_s.channel()

channel_b_s.queue_declare(queue=SERVER_TO_BROADCASTER)

def callback(ch,method,properties,body):
    print("received %r" % body)

channel_b_s.basic_consume(callback, queue=SERVER_TO_BROADCASTER, no_ack=True)

print('I am dummy android client and waiting for messages from the server....')

channel_b_s.start_consuming()

