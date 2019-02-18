import mongo_file as mongo
import esl_controller as esl
import event_listener_thread as conf_thread
import os
import json
import broadcaster_publisher
import fs_config as config
import connectSQL
from pydub import AudioSegment
import datetime
import sched
import time
import threading
import portal_app_update as portal



def update_broadcaster_database(data):

    if mongo.insert_update_broadcaster_static_info(data):
        return True
    else:
        return False

def get_notification_data(data):
    phoneno = data['broadcaster']
    
    data = mongo.get_notifications(phoneno)
    print("data is ",str(data))
 #  json_obj = '{"objective":"notify", "data":'+str(json.dumps(data))+'"}'
 #   print("json to be sent", json_obj)
    return data
    #broadcaster_publisher.send(json_obj)
    #return True


def get_cohort_size(cohort_id):
    members_phone_list =  connectSQL.get_listeners(cohort_id)
    #print("size of cohort is ", len(members_phone_list))	
    if members_phone_list:
	return len(members_phone_list)
    else:
	return "none"


def log_broadcaster_content_listen_data(data):
    if mongo.insert_broadcaster_content_listen_data(data):
	return True
    else:
	return False

def get_file_duration(filepath):

    if filepath[-3:] == 'wav':
    	audio_obj = AudioSegment.from_wav(filepath)
    elif filepath[-3:] == 'mp3':
        audio_obj = AudioSegment.from_mp3(filepath)
    #this is in miliseconds
    return len(audio_obj)
    


def get_filename(filepath):

    path_components = filepath.split('/')
    filename_with_ext = path_components[len(path_components)-1]
    filename_without_ext = filename_with_ext[:-4]
    return filename_without_ext



def get_show_playback_metadata(data):
    show_id = data['show_id']
    
    
    #if connectSQL.get_content_status(show_id) != "none":
    content_path = get_show_content_path(show_id)
    content_dur = get_file_duration(content_path)
    content_name = get_filename(content_path)
    content_local_name = connectSQL.get_upcoming_show_localized_topic_name(data['cohort_id'])  


    #computing duration
    QA1_filepath = portal.get_show_QA1_filepath(show_id)
    #if QA1_filepath == "none":
#	return "none"
    QA1_localname = portal.get_show_QA1_localname(show_id)
#    if QA1_localname == "none":
#	return "none"
    QA2_filepath = portal.get_show_QA2_filepath(show_id)
#    if QA2_filepath == "none":
#	return ""
    QA2_localname = portal.get_show_QA2_localname(show_id)
#    if QA2_localname == "none":
#	return

#    q2 = portal.get_show_question2_filepath(show_id)
 #   a2 = portal.get_show_answer2_filepath(show_id)
    #q3 = portal.get_show_question3_filepath(show_id)
    #a3 = portal.get_show_answer3_filepath(show_id)

    QA1_fullpath = config.content_base_dir + QA1_filepath
    QA1_dur = get_file_duration(QA1_fullpath)
    QA1_filename = get_filename(QA1_fullpath)

    QA2_fullpath = config.content_base_dir + QA2_filepath
    QA2_dur = get_file_duration(QA2_fullpath)
    QA2_filename = get_filename(QA2_fullpath)

  #  q2_fullpath = config.content_base_dir + q2.split('-')[1][1:]
   # q2_dur = get_file_duration(q2_fullpath)
   # q2_filename = get_filename(q2_fullpath)

   # a2_fullpath = config.content_base_dir + a2.split('-')[1][1:]
   # a2_dur = get_file_duration(a2_fullpath)
   # a2_filename = get_filename(a2_fullpath)

#    q3_fullpath = config.content_base_dir + q3.split('-')[1][1:]
#    q3_dur = get_file_duration(q3_fullpath)
#    q3_filename = get_filename(q3_fullpath)

#    a3_fullpath = config.content_base_dir + a3.split('-')[1][1:]
#    a3_dur = get_file_duration(a3_fullpath)
#    a3_filename = get_filename(a3_fullpath)


    

#hardcoding for now
    send_data = { 'objective' : 'show_playback_metadata_response',
                  'media': [{'type' : 'content','order': '1' , 'duration' : content_dur, 'name' : content_local_name},
  			{ 'type' : 'QA', 'order': '2', 'duration' : QA1_dur, 'name' : QA1_localname},
			 {'type' : 'QA', 'order': '3','duration' : QA2_dur, 'name' : QA2_localname}]
		} 

    return send_data

    """
    if portal.get_show_feedback_file(show_id) != "none":
        feedback = 'yes'
    else:
	feedback = 'no'
    
    if connectSQL.get_content_status(show_id) != "none":	
	content = 'yes'
    else:
	content = 'no'

    send_data = { 'objective' : 'show_playback_metadata_response',
                  'feedback' : feedback,
                  'show_content' : content,
                }
    """
    return send_data
 



def app_install(data):

    broadcaster = data['broadcaster']
    cohort_id = connectSQL.get_cohortID_from_broadcasterno(broadcaster)
    status = mongo.insert_app_install_data(data)
    return cohort_id


def show_polling(data):
    if mongo.insert_show_polling_logs(data):
        return True
    else:
        return False

   
def polling(show_id , phone_number, digit_pressed, poll_id , action):
    new_data = { 'show_id' : show_id,
		 'phone_no' : phone_number,
		 'digit_pressed' : digit_pressed,
		 'poll_id' : poll_id,
		 'action' : action}

    mongo.insert_user_polling_logs(new_data)

def insert_listeners_conference_dtmf_events(objective, show_id , conference_name, cohort_id, phone_number, digit_pressed, case):
    new_data = { 'objective' : objective, 
		 'show_id' : show_id,
		 'conference_name' : conference_name,
		 'phone_no' : phone_number,
  		 'cohort_id' : cohort_id,
                 'digit_pressed' : digit_pressed,
		 'case' : case}

    mongo.insert_listeners_conference_dtmf_events(new_data)

def freeswitch_conf_mute_unmute_logging(show_id, conference_name, cohort_id, phone_number, objective, dtmf):

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    new_data = { 'objective' : objective,	
		 'show_id' : show_id,
                 'cohort_id' : cohort_id,
                 'phone_number' : phone_number,
                 'dtmf' :  dtmf,
		 'conference_name' : conference_name,
                 'timestamp' : now}
    mongo.insert_user_mute_unmute_freeswitch_logs(new_data)

def freeswitch_conf_speak_event_logging(objective, show_id, conference_name, cohort_id, phone_number):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    new_data = {'objective' : objective, 
		'show_id' : show_id,
		'conference_name' : conference_name,
                'phone_no' : phone_number,
                'cohort_id' : cohort_id,
                'timestamp' : now}
    mongo.insert_user_speak_freeswitch_logs(new_data)

def pause_play_audio(data):
#    show_id = data['show_id']
    conference_name = data['conference_name']

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    new_data = {'objective' : "show_play_pause_media",
                'show_id' : data['show_id'],
                'conference_name' : data['conference_name'],
                'cohort_id' : data['cohort_id'],
		'media_order' : data['media_order'],
                'timestamp' : now}

    mongo.insert_play_pause_stats(new_data)
    return esl.pause_play_audio_conference(conference_name)



def get_show_content_path(show_id):

    relative_file = connectSQL.get_content_for_show(show_id)
    print("file received is ", relative_file)

    content_base_dir= config.content_base_dir
    absolute_path = content_base_dir + relative_file
    print("absolute path is ", absolute_path)
    return str(absolute_path)



def get_show_feedback_path(show_id):

    relative_file = portal.get_show_feedback_file(show_id)
    if relative_file != 'none':
	
        print("file received is ", relative_file)

	content_base_dir= config.content_base_dir
    	absolute_path = content_base_dir + relative_file
        print("absolute path is ", absolute_path)
        return str(absolute_path)
    else:
	return "none"


def get_show_media(show_id,media_order):

    if media_order == '1':
	absolute_path = get_show_content_path(show_id)
        if absolute_path == 'none':
            return False
        else:
            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")

            new_data = {'objective' : "start_play_show_content",
                    'show_id' : data['show_id'],
                    'conference_name' : data['conference_name'],
                    'cohort_id' : data['cohort_id'],
		    'media_order' : data['media_order'],
                    'timestamp' : now}

            mongo.insert_play_pause_stats(new_data)

            value = esl.play_audio_conference(conference_name, absolute_path)
            return True

    else:
	if media_order == '2':

	    QA1_filepath = portal.get_show_QA1_filepath(show_id)

	elif media_order == '3':

	    QA2_filepath = portal.get_show_QA2_filepath(show_id)    

	now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        new_data = {'objective' : "start_play_show_QA",
                    'show_id' : data['show_id'],
                    'conference_name' : data['conference_name'],
                    'cohort_id' : data['cohort_id'],
	   	    'media_order' : media_order,
                    'timestamp' : now}

        mongo.insert_play_pause_stats(new_data)

        value = esl.play_audio_conference(conference_name, QA1_filepath)
        return True


def play_content_audio(data):
    show_id = data['show_id']

    media_order = data['media_order']

    if media_order == '1':
	file_path = get_show_content_path(show_id)

    if media_order == '2':
        file_path = portal.get_show_QA1_filepath(show_id)
	file_path = config.content_base_dir + file_path

    if media_order == '3':
        file_path = portal.get_show_QA2_filepath(show_id)
        file_path = config.content_base_dir + file_path
	
    
    conference_name = data['conference_name']
#    absolute_path = get_show_content_path(show_id)
    if file_path  == 'none':
        return False
    else:
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        new_data = {'objective' : "start_play_show_media",
                    'show_id' : data['show_id'],
                    'conference_name' : data['conference_name'],
                    'cohort_id' : data['cohort_id'],
		    'media_type' : data['type'],
		    'media_order' : data['media_order'],
		    'file_path' : file_path,
                    'timestamp' : now}

        mongo.insert_play_pause_stats(new_data)

        value = esl.play_audio_conference(conference_name, file_path)
	return True


def play_feedback_audio(data):
    show_id = data['show_id']
    conference_name = data['conference_name']
    absolute_path = get_show_feedback_path(show_id)

    if absolute_path == 'none':
        return False
    else:
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        new_data = {'objective' : "start_play_show_feedback",
                'show_id' : data['show_id'],
                'conference_name' : data['conference_name'],
                'cohort_id' : data['cohort_id'],
                'timestamp' : now}

        mongo.insert_play_pause_stats(new_data)

        value = esl.play_audio_conference(conference_name, absolute_path)
	return True



def stop_audio(data):
    conference_name = data['conference_name']
    return esl.stop_audio_conference(conference_name)

def poll_results(data):

    status = mongo.get_poll_results(data['show_id'] , data['poll_id'])
    return status


def insert_show_trailer_call_logs(objective, show_id, cohort_id, phone_number, call_attempt):

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {'objective' : objective,
            'show_id' :  show_id,
            'phone_number' : phone_number,
            'cohort_id' : cohort_id,
	    'call_attempt' : call_attempt,
            'timestamp' : now}

    mongo.insert_show_trailer_call_logs(data)



def update_show_status(data):
    show_id = data['show_id']
    
    #status = data['status']
#    print(status)
    #if status == "done":
#	print("done case")
#	status_value = 1
#    else:

#	status_value = 0
    ret_value = connectSQL.update_show_status(show_id, 1)
    status = portal.update_show_recordings_in_portal(show_id)
    if ret_value == 'OK':
	return True
    else:
	return False




def create_show(data):

    split_timestamp = data['time_of_airing'].split();
    
    split_date = split_timestamp[0]
    split_date_again = split_date.split('/') 
    split_time = split_timestamp[1]
    split_time_again = split_time.split(':')
    
    show_id = data['broadcaster_phoneno'] +  '_' + split_date_again[0] + '_' + split_date_again[1] + '_' + split_date_again[2] + '_'  + split_time_again[0] + '_' + split_time_again[1] + '_'  + split_time_again[2]   

    new_data = { 'audio_name' : data['audio_name'],
                 'broadcaster_phoneno' : data['broadcaster_phoneno'],
                 'list_of_listeners' : data['list_of_listeners'],
                 'time_of_airing' : data['time_of_airing'],
                 'show_hosting_status' : data['show_hosting_status'],
                 'timestamp' : data['timestamp'],
                 'show_id' : show_id,
                 'objective' : data['objective']}            
                 
    if mongo.insert_show_stats(new_data):
        return True
    else:
        return False   

"""
    if mongo.insert_show_stats(data):
        return True
    else:
        return False        
"""

def get_show(data):
   
    broadcaster_phone_no = data['broadcaster_phoneno']
    print("show populate data is", mongo.get_matching_broadcasters(broadcaster_phone_no))
    return mongo.get_matching_broadcasters(broadcaster_phone_no)

       
def play_pause(data):
    if mongo.insert_play_pause_stats(data):
        return True
    else:
        return False

def flush_query(data):
    if mongo.insert_QA_round_flush(data):	
	return True
    else:
	return False
    
def query(data):
    if mongo.insert_asha_query_stats(data):
        return True
    else:
        return False

def like(data):
    if mongo.insert_asha_like_stats(data):
        return True
    else:
        return False
    
def get_show_status(show_name):

    status = mongo.get_show_status(show_name)
    return status


def del_listener(incoming_json):
    show_name = incoming_json['show_id']
    phone = incoming_json['broadcaster_phoneno']

    status_add = mongo.insert_del_listener_stats(incoming_json)
    status_delete = mongo.del_listener(show_name,phone)
    
    if status_add and status_delete:
        return True
    else:
        return False
    
def del_all_listener(incoming_json):
    show_name = incoming_json['show_id']

    status_add = mongo.insert_del_all_listener_stats(incoming_json)
    status_delete = mongo.del_all_listener(show_name)
    
    if status_add and status_delete:
        return True
    else:
        return False

def check_trailer(incoming_json):
    show_name = incoming_json['show_name']
    
    trailer_path = "/usr/local/freeswitch/recordings/"+show_name+"/trailer/trailer.wav"
    if os.path.isfile(trailer_path):
        return True
    else:
        return False
    
def play_trailer(incoming_json):
    show_name = incoming_json['show_name']

    status_add = mongo.insert_play_trailer_stats(incoming_json)
    
    trailer_path = "/usr/local/freeswitch/recordings/"+show_name+"/trailer/trailer.wav"

##    if os.path.isfile(trailer_path):
##        if esl.play_trailer_host(studio):
##            return True
##        else:
##            return False
##    else:
##        return False
        
def delete_trailer(incoming_json):
    show_name = incoming_json['show_name']

    status_add = mongo.insert_delete_trailer_stats(incoming_json)
    
    trailer_path = "/usr/local/freeswitch/recordings/"+show_name+"/trailer/trailer.wav"

##    if os.path.isfile(trailer_path):
##        os.remove(trailer_path)
##        if not os.path.isfile(trailer_path):
##            return True
##        else:
##            return False
   
def get_broadcaster(show_name):
    #show_name = incoming_json['show_id']
    broadcaster = mongo.get_broadcaster_from_db(show_name)
    return broadcaster

def call_conference_host(broadcaster_no, conf_id, recording_file_path):
#    ret_val = esl.add_broadcaster_to_conference(broadcaster_no, config.locale, conf_id, "endconf", "conference_host", recording_file_path)
    ret_val = esl.add_broadcaster_to_conference(broadcaster_no, config.locale, conf_id, "unmute", "conference_host", recording_file_path)

    if "OK" in ret_val:
#        print("returning true")
        return True
    else:
#	print("returning False")
	return False


def call_listener(incoming_json, recording_path):
    show_id = incoming_json['show_id']
    cohort_id = incoming_json['cohort_id']
    conference_name = incoming_json['conference_name']
    listeners = connectSQL.get_listeners(cohort_id)
    
   # status_add = mongo.insert_listener_show_call_logs(incoming_json)
   # ashas = mongo.get_ashas_from_db(show_name)
   # print("ASHA list fetched fron DB is ", str(listeners))

    for listener in listeners:
        print("calling listener with phone number",str(listener[0]))
	
        dial_result = esl.add_listener_to_conference(str(listener[0]), show_id, config.locale, conference_name, cohort_id, "mute","conference_start", recording_path, "none")
	
    if dial_result == "none":
	return False
    else:	
    	return True 

def insert_listener_show_call_logs(objective, show_id, conference_name, phone_number, cohort_id):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {'objective' : objective,
            'show_id' :  show_id,
            'phone_number' : phone_number,
            'cohort_id' : cohort_id,
            'conference_name' : conference_name,
            'timestamp' : now}

    mongo.insert_listener_show_call_logs(data)



def insert_listener_conf_redial_call_logs(objective, show_id, conference_name, phone_number, cohort_id, call_attempt):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {'objective' : objective,
            'show_id' :  show_id,
            'phone_number' : phone_number,
            'cohort_id' : cohort_id,
            'conference_name' : conference_name,
	    'call_attempt' : call_attempt,
            'timestamp' : now}

    mongo.insert_listener_show_call_logs(data)








def insert_broadcaster_show_call_logs(objective, show_id, conference_name, phone_number, cohort_id, call_attempt):


    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {'objective' : objective,
            'show_id' :  show_id,
            'phone_number' : phone_number,
            'cohort_id' : cohort_id,
            'conference_name' : conference_name,
	    'call_attempt' : call_attempt,
            'timestamp' : now}

    mongo.insert_broadcaster_show_call_logs(data)



def get_active_participants_phone(conference_name):
#    conference_name = incoming_json['conference_name']
    member_phonelist= esl.get_conference_participants_phone(conference_name)
    return member_phonelist
#    for member in member_data:
#	print('member entry is ', member)
#    print(member_data)

def mute_unmute(incoming_json):

    show_name = incoming_json['show_id']
    phoneno = incoming_json['listener_phoneno']
    mode = incoming_json['objective']
    
    
    conference_name = incoming_json['conference_name']

    status_add = mongo.insert_mute_unmute_logs(incoming_json)
    
    members_list = esl.get_conference_participants(conference_name)

    if members_list is not None:
       
        member_id = esl.get_member_id_by_phone_number(members_list, phoneno)        
	if member_id:
	        print("member id  of phone "+phoneno+" is "+ str(member_id))
        	task_result = esl.set_mode(conference_name, member_id, mode)

        	if task_result:           
            		return True
        	else:
            		return False
	else:
		#trying again
		print('member list fetched is none')
		members_list = esl.get_conference_participants(conference_name)
		member_id = esl.get_member_id_by_phone_number(members_list, phoneno)
		if member_id:
			print("member id  of phone "+str(phoneno)+" is "+ str(member_id))
			task_result = esl.set_mode(conference_name, member_id, mode)
			if task_result:
				return True
			else:
				return False
		else:
			return False
            
    else:
	print("conference member list is returned as None")
        return False
    







def insert_freewitch_show_end_logs(objective, show_id, conference_name, cohort_id):

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {'objective' :  objective,
	    'show_id' : show_id,
            'conference_name' : conference_name,
            'cohort_id' : cohort_id,
	    'timestamp' : now
            }
    
    result = mongo.insert_freewitch_show_end_logs(data)
    if result:
        return True
    else:
        return False


def end_show_call(incoming_json):
    #mongo.insert_app_end_show_logs(incoming_json)
    conference_name = incoming_json['conference_name']
    show_id = incoming_json['show_id']
    cohort_id = incoming_json['cohort_id']

    val  = insert_freewitch_show_end_logs("conference_end", show_id, conference_name, cohort_id)
    
    if esl.end_conference(conference_name):
        print('success ending')
        return True
    else:
        print('error ending')
        return False
