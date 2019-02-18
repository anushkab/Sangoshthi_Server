#!/usr/bin/env python

#This file is for accepting requesting from the android app of the show host

import sys
sys.path.append('/home/sangoshthi/sangoshthi_new/analytics/')
import show_statistics

import pika
import json
import yaml
import controller as ctrl
import event_listener_thread
import s_a as server_to_asha
import broadcaster_publisher
import datetime
import os, sys
import fs_config
import datetime
import connectSQL
import mongo_file as mongo
import portal_app_update as portal



#import threading
TRAINER_TO_SERVER = "broadcaster_to_server_ivr"


# rabbitmq declarations
credentials_b_s = pika.PlainCredentials('sangoshthi', 'sangoshthi')
parameters_b_s = pika.ConnectionParameters('192.168.2.71',5672,'/',credentials_b_s)

# broadcaster to server
connection_b_s = pika.BlockingConnection()
channel_b_s = connection_b_s.channel()

channel_b_s.queue_declare(queue=TRAINER_TO_SERVER)

#broadcaster_no = "xyz"

show_thread_dict = {}
show_conf_recording_path_dict = {}
#mylock = threading.Lock()





def callback_b_s(ch, method, properties, body):
    
    #print('packet eithout utf-8: ')
    
#    if isinstance(body, unicode):
#        print('unicode')    
#        print(str(body))
    try:
        incoming_json = json.loads(body.encode('utf-8'))
    except:
	print('error in encoding into utf-8')
	incoming_json = json.loads(body)

    print("msg received from broadcaster")    
    #print(incoming_json)
   # broadcaster_no = "xyz"
    # NETWORK COMMANDS

    msg = 'EMPTY'

    data = {'objective' : 'command_not_found'}
    # create a new show
    if incoming_json['objective'] == 'broadcaster_basic_info':
        if ctrl.update_broadcaster_database(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'
	json_data = json.dumps(data)
	broadcaster_publisher.send(json_data , broadcaster_no)

    elif incoming_json['objective'] == 'start_polling':
        broadcaster_no = ctrl.get_broadcaster(incoming_json['show_id'])
	event_listener_thread.start_polling = True
	event_listener_thread.options = incoming_json['no_options']
	event_listener_thread.pollid = incoming_json['poll_id']

	if ctrl.show_polling(incoming_json):
           msg = 'OK'
	else:
	   msg = 'FAIL'
        json_data = json.dumps(data)
	broadcaster_publisher.send(json_data , broadcaster_no,"1")

    elif incoming_json['objective'] == 'stop_polling':
 	broadcaster_no = incoming_json['broadcaster']
        event_listener_thread.stop_polling = True
        data = {'objective' : 'command_found'}
        json_data = json.dumps(data)
	broadcaster_publisher.send(json_data , broadcaster_no, "1")

    elif incoming_json['objective'] == 'flush_callers':

        broadcaster_no = incoming_json['broadcaster']
	ret_val = ctrl.flush_query(incoming_json)
        show_thread_dict[broadcaster_no].flush_dtmf_members_list()
        print('show thread data is ', show_thread_dict)
        msg = 'OK'
        data = {'objective' : 'flush_callers_ack', 'info': msg}
        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")


    elif incoming_json['objective'] == 'get_upcoming_show':
        cohort_id = incoming_json['cohort_id']

        show_id = connectSQL.get_upcoming_showID(cohort_id)
	if show_id != "none": 
            timeofairing = connectSQL.get_upcoming_show_time(cohort_id)
            topic =  connectSQL.get_upcoming_show_topic(cohort_id)
	    local_name = connectSQL.get_upcoming_show_localized_topic_name(cohort_id)
	    #local_name = unicode(local_name[0], encoding='utf-8')
            print('showid is '+show_id+'time '+timeofairing+' topic '+topic+'local name is'+local_name)

  	    data = {'objective' : 'upcoming_show_data', 'show_id' : show_id, 'time_of_airing' : timeofairing, 'topic' : topic, 'local_name' : local_name}

	else:
	    
  	    data = {'objective' : 'upcoming_show_data', 'show_id' : 'none', 'time_of_airing' : 'none', 'topic' : 'none', 'local_name' : 'none'}
  	

        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , incoming_json['broadcaster'], "2")

    elif incoming_json['objective'] == 'get_show_id_for_gallery':

        cohort_id = incoming_json['cohort_id']

        show_id = connectSQL.get_upcoming_showID(cohort_id)
        if show_id != "none":
            timeofairing = connectSQL.get_upcoming_show_time(cohort_id)

            topic =  connectSQL.get_upcoming_show_topic(cohort_id)
            print('showid is '+show_id+'time '+timeofairing+' topic '+topic)

	    content_id = connectSQL.get_contentID_for_show(show_id)
            print('content id is ', content_id)

            data = {'objective' : 'get_show_id_for_gallery_ack', 'show_id' : show_id, 'time_of_airing' : timeofairing, 'topic' : topic, 'content_id' : content_id}

        else:

            data = {'objective' : 'get_show_id_for_gallery_ack', 'show_id' : 'none', 'time_of_airing' : 'none', 'topic' : 'none'}
        print(str(data))

        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , incoming_json['broadcaster'], "2")


    elif incoming_json['objective'] == 'app_install_notify':
        broadcaster_no = incoming_json['broadcaster']

        cohort_id = ctrl.app_install(incoming_json)
        if cohort_id != "none":
	    size = ctrl.get_cohort_size(cohort_id)
	    if size != "none":
                data = {"objective" : "configuration_data", "cohort_id" : cohort_id, "cohort_size" : str(size)}
	    else:
		data = {"objective" : "configuration_data", "cohort_id" : cohort_id, "cohort_size" : "0"}
	else:
            data = {"objective" : "configuration_data", "cohort_id" : "-1", "cohort_size" : "-1"}

        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "2")
          

    elif incoming_json['objective'] == 'get_notifications':
	broadcaster_no = incoming_json['broadcaster']
        msg = ctrl.get_notification_data(incoming_json)
        if msg != "none":
	    data = {"objective" : "notify", "info" : msg}
	else:
	    data = {"objective" : "notify", "info" : "-1"}
        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "2")
        


    elif incoming_json['objective'] == 'play_show_media':
        broadcaster_no = incoming_json['broadcaster']
        if ctrl.play_content_audio(incoming_json):
            msg = 'OK'

        else:
            msg = 'FAIL'

        data = {"objective" : "play_show_media_ack", "info" : msg}
        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")
        
	#setting the media flag and order in the event listener thread of the conference
	show_thread_dict[broadcaster_no].set_playback_flag(incoming_json['type'], incoming_json['media_order'])
       

        #broadcaster_publisher.send(json_data , broadcaster_no)



    elif incoming_json['objective'] == 'pause_play_content':
        broadcaster_no = incoming_json['broadcaster']
        if ctrl.pause_play_audio(incoming_json):
            msg = 'OK'

        else:
            msg = 'FAIL'

            data = {"objective" : "pause_play_audio_ack", "info" : msg}
            json_data = json.dumps(data)
            broadcaster_publisher.send(json_data , broadcaster_no, "1")

        #broadcaster_publisher.send(json_data , broadcaster_no)

    elif incoming_json['objective'] == 'stop_content':
        broadcaster_no = incoming_json['broadcaster']
        if ctrl.stop_audio(incoming_json):
            msg = 'OK'
	else:
	    msg = 'FAIL'
	
	data = {"objective" : "stop_content_ack", "info" : msg}
        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")

        #broadcaster_publisher.send(json_data , broadcaster_no)


    # create a new show
    elif incoming_json['objective'] == 'create_show':
        if ctrl.create_show(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'        
        #broadcaster_publisher.send(json_data , broadcaster_no)


    # get show status if finished or not
    elif incoming_json['objective'] == 'get_show_status':        
        msg = ctrl.get_show_status(incoming_json['show_id'])
        # broadcaster_publisher.send(json_data , broadcaster_no)    
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

        #broadcaster_publisher.send(json_data , broadcaster_no)
    # delete all listeners for a specific show and also add its entry in a new table for logging purpose
    elif incoming_json['objective'] == 'del_all_listener':
        if ctrl.del_all_listener(incoming_json):
            msg = "OK"
        else:
            msg = "FAIL"

    # check the status of trailer if it is uploaded or not
    elif incoming_json['objective'] == "check_trailer":
        if ctrl.check_trailer(incoming_json['show_id']):
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
    elif incoming_json['objective'] == 'start_show':
	#broadcaster_no = ctrl.get_broadcaster(incoming_json['show_id'])
        broadcaster_no = incoming_json['broadcaster']
        cohort_id = incoming_json['cohort_id']
        print("start show request")

        now = datetime.datetime.now()
        now = now.strftime("%Y_%m_%d_%H_%M_%S")


	#creating directories to store the show recordings
	show_id = incoming_json['show_id']
        conf_name = show_id + '_' + now

        show_dir = fs_config.recording_dir + show_id 
        conf_dir = show_dir + "/" + conf_name
        recording_file_path = conf_dir + "/" + show_id
	
	
        if not os.path.exists(show_dir):
            os.makedirs(show_dir, 0755)
     
        if not os.path.exists(conf_dir):
            os.makedirs(conf_dir, 0755) 


        #if not os.path.exists(recording_file_path):
        #    os.makedirs(conf_dir, 0755)

           
	#calling the host person first
        if ctrl.call_conference_host(broadcaster_no,conf_name,recording_file_path):
	    print('CONF NAMEEEE is '+conf_name)
	    print('recording file path  is '+recording_file_path)

	    if broadcaster_no not in show_thread_dict.keys():
		print('CONF NAMEEEE is '+conf_name)            

                show_thread_dict[broadcaster_no] = event_listener_thread.EventListenerThread(incoming_json['show_id'], cohort_id, conf_name, broadcaster_no, show_thread_dict)
                show_thread_dict[broadcaster_no].start()
	        show_thread_dict[broadcaster_no].set_conf_recording_path(recording_file_path)
	        show_conf_recording_path_dict[broadcaster_no] = recording_file_path
                msg =  conf_name
	        mongo.insert_show_conference_timestamps(incoming_json)

        else:
            msg = "FAIL"          

        data = {'objective' : 'start_show_response', 'info' : msg}

        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")

    # call ashas
    elif incoming_json['objective'] == 'dial_listeners':
        broadcaster_no = incoming_json['broadcaster']
	cohort_id = incoming_json['cohort_id']
	print('broadcaster no is ', broadcaster_no)

        #checking is thread is alive to counter cases when the host killed the app and restarted at this stage
	if broadcaster_no in show_thread_dict.keys():
	    show_thread_dict[broadcaster_no].set_dial_listeners_flag()
	else:
	    print('thread has ended')


	get_cohort_members_name_phone_mapping = connectSQL.get_cohort_members_name_phone_mapping(cohort_id)
	json_array = {}
	for member in get_cohort_members_name_phone_mapping:
#	     json_array.append({member[0]:member[1]})
	    json_array[member[0]] = member[1]

        if ctrl.call_listener(incoming_json, show_conf_recording_path_dict[broadcaster_no]):

            msg = 'OK'
	    #show_thread_dict[broadcaster_no].set_dial_listeners_flag()
	    mongo.insert_show_conference_timestamps(incoming_json)
	    data = {'objective' : 'dial_listeners_response', 'cohort_members_phone_name_mapping' : json_array}
	
	else:
            msg = 'FAIL'
	    data = {'objective' : 'dial_listeners_response', 'info' : msg}

        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")


    #get playback content metadata
    elif incoming_json['objective'] == 'show_playback_metadata':
        broadcaster_no = incoming_json['broadcaster']
	data = ctrl.get_show_playback_metadata(incoming_json)
	#if data
        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")


    # set asha mute/unmute 
    elif incoming_json['objective'] == 'mute':
        broadcaster_no = incoming_json['broadcaster']
        listener_phoneno = incoming_json['listener_phoneno']
	#to keep track of unmute mute multiple in same QA
        turn = incoming_json['turn'] 
	show_thread_dict[broadcaster_no].QA_recording_action(listener_phoneno, "stop", turn)
        
	if ctrl.mute_unmute(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'


        data = {'objective' : 'mute_unmute_ack', 'info' : msg, "listener_phoneno" : listener_phoneno}

        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")
	

    elif incoming_json['objective'] == 'unmute':
	broadcaster_no = incoming_json['broadcaster']
        listener_phoneno = incoming_json['listener_phoneno']
	turn = incoming_json['turn']
	print('turn is', str(turn))
        show_thread_dict[broadcaster_no].QA_recording_action(listener_phoneno, "start", turn)

        if ctrl.mute_unmute(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'

        data = {'objective' : 'mute_unmute_ack', 'info' : msg, "listener_phoneno" : listener_phoneno}

        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")


    elif incoming_json['objective'] == 'play_feedback':

        broadcaster_no = incoming_json['broadcaster']
        if ctrl.play_feedback_audio(incoming_json):
            msg = 'OK'

        else:
            msg = 'FAIL'

        data = {"objective" : "play_feedback_ack", "info" : msg}
        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")
        show_thread_dict[broadcaster_no].set_playback_flag("feedback")


    # get active participants
    elif incoming_json['objective'] == 'get_active_participants':
	broadcaster_no = ctrl.get_broadcaster(incoming_json['show_id'])
        participants = ctrl.get_active_participants(incoming_json)
        if participants:
            msg = participants
        else:
            msg = 'FAIL'


    elif incoming_json['objective'] == 'update_show_status':
	broadcaster_no = incoming_json['broadcaster']
	show_id = incoming_json['show_id']

        if ctrl.update_show_status(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'
        data = {"objective" : "update_show_status_ack", "info" : msg}
        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")
	portal.update_show_recordings_in_portal(show_id)
	


    # end the show  
    elif incoming_json['objective'] == 'end_show_call':
	broadcaster_no = incoming_json['broadcaster']
        show_id = incoming_json['show_id']
        conference_name = incoming_json['conference_name']
        cohort_id = incoming_json['cohort_id']

	#stopping the conference thread for this conference identified by the broadcaster number
	if broadcaster_no in show_thread_dict.keys():
            if ctrl.end_show_call(incoming_json):
                msg = 'OK'
	    else:
                msg = 'FAIL'
	    if show_thread_dict[broadcaster_no].is_alive():
                show_thread_dict[broadcaster_no].stop()
	    else:
	        print('Thread already crashed')
	else:
	    msg = 'OK'
	data = {"objective" : "end_show_call_ack", "info" : msg}
	json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "1")
	#porting statistics computation to portal to avoid crashing of the server
#	show_statistics.compute_show_stats(show_id,conference_name, cohort_id)

    elif incoming_json['objective'] == 'broadcaster_content_listen_event':

        broadcaster_no = incoming_json['broadcaster']
	packet_id = incoming_json['packet_id']
        if ctrl.log_broadcaster_content_listen_data(incoming_json):
            msg = 'OK'
        else:
            msg = 'FAIL'

        data = {"objective" : "broadcaster_content_listen_event_ack", "info" : msg, "packet_id" : packet_id}
        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , broadcaster_no, "2")





    #data = {"objective" : "ack", "info" : msg}
    #json_data = json.dumps(data)
    #print(json_data)

    
   # broadcaster_no = ctrl.get_broadcaster(incoming_json['show_id'])
   # broadcaster_publisher.send(json_data , broadcaster_no)
    
channel_b_s.basic_consume(callback_b_s, queue=TRAINER_TO_SERVER, no_ack=True)

print('Waiting for Messages from the broadcaster...')

channel_b_s.start_consuming()
