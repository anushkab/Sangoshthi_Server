import pika
import json
import yaml



#SERVER_TO_BROADCASTER = 'server_to_broadcaster_ivr_9810473190'

credentials = pika.PlainCredentials('sangoshthi', 'sangoshthi')
parameters = pika.ConnectionParameters('192.168.2.71',5672,'/',credentials)

def send(body , phoneno, priority):
    SERVER_TO_BROADCASTER = 'server_to_broadcaster_ivr_' + str(phoneno)
    #print 'queue name is :' + SERVER_TO_BROADCASTER

    connection_s_b = pika.BlockingConnection()
    channel_s_b = connection_s_b.channel()

    channel_s_b.queue_declare(queue=SERVER_TO_BROADCASTER)
  
    if priority == '1':
	#print "priority case"
        properties = pika.BasicProperties(expiration = '20000')
	print("data to be published", body)
	channel_s_b.basic_publish( exchange='', routing_key=SERVER_TO_BROADCASTER,  body=body, properties = properties)
    else:
	print("data to be published non priority", body)
	channel_s_b.basic_publish( exchange='', routing_key=SERVER_TO_BROADCASTER,  body=body)

    connection_s_b.close()
