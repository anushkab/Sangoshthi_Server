import pika

SERVER_TO_BROADCASTER = 'server_to_broadcaster'

credentials = pika.PlainCredentials('root', 'root')
parameters = pika.ConnectionParameters('192.168.2.71',5672,'/',credentials)

def send(body):
    connection_s_b = pika.BlockingConnection(parameters)
    channel_s_b = connection_s_b.channel()

    channel_s_b.queue_declare(queue=SERVER_TO_BROADCASTER)
   
    channel_s_b.basic_publish( exchange='', routing_key=SERVER_TO_BROADCASTER, body=body)

    connection_s_b.close()
