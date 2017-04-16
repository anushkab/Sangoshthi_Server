import pika

SERVER_TO_ASHA = 'server_to_asha'

credentials = pika.PlainCredentials('root', 'root')
parameters = pika.ConnectionParameters('192.168.2.71',5672,'/',credentials)

def send(body):
    connection_s_a = pika.BlockingConnection(parameters)
    channel_s_a = connection_s_a.channel()

    channel_s_a.queue_declare(queue=SERVER_TO_ASHA)
   
    channel_s_a.basic_publish( exchange='', routing_key=SERVER_TO_ASHA, body=body)

    connection_s_a.close()
