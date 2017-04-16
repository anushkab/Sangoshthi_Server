#!/usr/bin/env python
import pika
import json
import yaml
import controller as ctrl
import s_b as server_to_broadcaster

ASHA_TO_SERVER = "asha_to_server"

# rabbitmq declarations
credentials_a_s = pika.PlainCredentials('root', 'root')
parameters_a_s = pika.ConnectionParameters('127.0.0.1',5672,'/',credentials_a_s)

## asha to server
connection_a_s = pika.BlockingConnection()
channel_a_s = connection_a_s.channel()

channel_a_s.queue_declare(queue=ASHA_TO_SERVER)

def callback_a_s(ch, method, properties, body):

    incoming_json = yaml.safe_load(body)

    print("msg received from asha")
    print(incoming_json)

    if(data['objective'] == "query"):
        if ctrl.query(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'
       
        server_to_broadcaster.send(body)
        
    elif(data['objective'] == "like"):
        if ctrl.like(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'
            
        server_to_broadcaster.send(body)
    
	
channel_a_s.basic_consume(callback_a_s, queue=ASHA_TO_SERVER, no_ack=True)

logger.info('Waiting for messages...')

channel_a_s.start_consuming()
