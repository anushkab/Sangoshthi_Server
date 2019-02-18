import pika
import json
import yaml


#SERVER_TO_BROADCASTER = 'server_to_broadcaster_ivr_show_9810473190'

credentials = pika.PlainCredentials('sangoshthi', 'sangoshthi')
parameters = pika.ConnectionParameters('192.168.2.71',5672,'/',credentials)

def send(body, phoneno):
    SERVER_TO_BROADCASTER = 'server_to_broadcaster_ivr_show_' + str(phoneno)
    print 'queue name is' + SERVER_TO_BROADCASTER
    connection_s_b = pika.BlockingConnection()
    channel_s_b = connection_s_b.channel()

    channel_s_b.queue_declare(queue=SERVER_TO_BROADCASTER)

    channel_s_b.basic_publish( exchange='', routing_key=SERVER_TO_BROADCASTER, body=body)

    connection_s_b.close()


