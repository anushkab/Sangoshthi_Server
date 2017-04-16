#!/usr/bin/env python
import pika
import json
import yaml
import controller as ctrl
import s_a as server_to_asha
import s_b as server_to_broadcaster

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("[b_s]")

BROADCASTER_TO_SERVER = "broadcaster_to_server"

# rabbitmq declarations
credentials_b_s = pika.PlainCredentials('root', 'root')
parameters_b_s = pika.ConnectionParameters('192.168.2.71',5672,'/',credentials_b_s)

# broadcaster to server
connection_b_s = pika.BlockingConnection()
channel_b_s = connection_b_s.channel()

channel_b_s.queue_declare(queue=BROADCASTER_TO_SERVER)

def callback_b_s(ch, method, properties, body):
    
    incoming_json = yaml.safe_load(body)
    
    logger.info("msg received from broadcaster")    
    logger.info(incoming_json)

    # NETWORK COMMANDS
    
    # create a new show
    if incoming_json['objective'] == 'create_show':
        if ctrl.create_show(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'        

    # play/pause commands
    elif incoming_json['objective'] == "play_pause":
        if ctrl.play_pause(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'
            
        server_to_asha.send(body)
        
    # flush query
    elif incoming_json['objective'] == "flush_query":
        if ctrl.flush_query(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'
            
        server_to_asha.send(body)

    # get show status if finished or not
    elif incoming_json['objective'] == 'get_show_status':        
        msg = ctrl.get_show_status(incoming_json['show_name'])
            
    # FREESWITCH COMMANDS

    # schedule the broadcast of the trailer and also add its entry in a new table for logging purpose
    elif incoming_json['objective'] == 'spread_word':        
        if ctrl.spread_word(incoming_json):
            msg = "OK"
        else:
            msg = "FAIL"

    # delete listener for a specific show and also add its entry in a new table for logging purpose
    elif incoming_json['objective'] == 'del_listener':
        if ctrl.del_listener(incoming_json):
            msg = "OK"
        else:
            msg = "FAIL"

    # delete all listeners for a specific show and also add its entry in a new table for logging purpose
    elif incoming_json['objective'] == 'del_all_listener':
        if ctrl.del_all_listener(incoming_json):
            msg = "OK"
        else:
            msg = "FAIL"

    # check the status of trailer if it is uploaded or not
    elif incoming_json['objective'] == "check_trailer":
        if ctrl.check_trailer(incoming_json['show_name']):
            msg = "OK"
        else:
            msg = "FAIL"
            
    # broadcaster plays the trailer and sees if its correct or not
    elif incoming_json['objective'] == "play_trailer":
        if ctrl.play_trailer(incoming_json):
            msg = "OK"
        else:
            msg = "FAIL"

    # broadcaster deletes the trailer 
    elif incoming_json['objective'] == "delete_trailer":
        if ctrl.delete_trailer(incoming_json):
            msg = "OK"
        else:
            msg = "FAIL"

    # call the broadcaster
    elif incoming_json['objective'] == 'call_broadcaster':

        if ctrl.call_broadcaster(incoming_json):
            msg = "OK"
        else:
            msg = "FAIL"          

        thread = event_listener_thread.EventListenerThread(incoming_json['show_name'])
        thread.start()

    # call ashas
    elif incoming_json['objective'] == 'call_listener':
            
        if ctrl.call_listener(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'

    # set asha mute/unmute 
    elif incoming_json['objective'] == 'mute/unmute':
        
        if ctrl.mute_unmute(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'

    # get active participants
    elif incoming_json['objective'] == 'get_active_participants':

        participants = ctrl.get_active_participants(incoming_json)
        if participants:
            msg = data
        else:
            msg = 'FAIL'

    # end the show  
    elif incoming_json['objective'] == 'end_show':

        if ctrl.end_show(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'


    data = {"objective" : "ack", "info" : msg}
    json_data = json.dumps(data)
    logger.debug(json_data)
    server_to_broadcaster.send(json_data)
    
channel_b_s.basic_consume(callback_b_s, queue=BROADCASTER_TO_SERVER, no_ack=True)

logger.info('Waiting for Messages...')

channel_b_s.start_consuming()
