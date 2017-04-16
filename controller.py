import MongoFile as mongo
import eslcontroller as esl
import os

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("[controller]")

def create_show(data):
    if mongo.insert_show_stats(data):
        return True
    else:
        return False        

def play_pause(data):
    if mongo.insert_play_pause_stats(data):
        return True
    else:
        return False

def flush_query(data):
    if mongo.insert_flush_query_stats(data):
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
    if mongo.get_show_status(show_name):
        return True
    else:
        return False

# doubt
def spread_word(incoming_json):

    show_name = incoming_json['show_name']
    date = incoming_json['date']
    time = incoming_json['time']

    mongo.insert_spread_word_stats(incoming_json)
    listener_list = mongo.get_ashas_from_db(show_name)

    for listener in listener_list:
        logger.debug(listener)
    
    #receives data in format: dd/mm/yyyy the default format of the android
	
    date_details = date.split("/")
    new_date_str = date_details[2] + "-" + date_details[1]+"-"+date_details[0]
    
    time_details = time.split(":")
    new_time_str = time_details[0]+":"+time_details[1]+":00"

    logger.debug(new_date_str , new_time_str)
    
##  for listener in listener_list: 
##        if esl.schedule_trailer(new_date_str,new_time_str,listener[0],show_name):
##            return_flag = True
##        else:
##            return_flag = False
##            break
##
    return True

def del_listener(incoming_json):
    show_name = incoming_json['show_name']
    phone = incoming_json['phone']

    status_add = mongo.insert_del_listener_stats(incoming_json)
    status_delete = mongo.del_listener(show_name,phone)
    
    if status_add and status_delete:
        return True
    else:
        return False
    
def del_all_listener(incoming_json):
    show_name = incoming_json['show_name']

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

   
def call_broadcaster(incoming_json):
    show_name = incoming_json['show_name']

    status_add = mongo.insert_call_broadcaster_stats(incoming_json)
    broadcaster = mongo.get_broadcaster_from_db(show_name)
    
    if broadcaster:
        esl.add_broadcaster_to_conference(broadcaster, show_name, "endconf","conference")
        return True
    else:
        return False

def call_listener(incoming_json):
    show_name = incoming_json['show_name']

    status_add = mongo.insert_call_listener_stats(incoming_json)
    ashas = mongo.get_ashas_from_db(show_name)

    for asha in ashas:
        esl.add_listener_to_conference(asha, show_name, "mute","conference")

    return True 

def get_active_participants(incoming_json):
    show_name = incoming_json['show_name']
    return esl.get_conference_participants(show_name)

def mute_unmute(incoming_json):

    show_name = incoming_json['show_name']
    phoneno = incoming_json['phone_no']
    mode = incoming_json['mode']

    status_add = mongo.insert_mute_unmute_stats(incoming_json)
    
    members_list = esl.get_conference_participants(show_name)

    if members_list is not None:
       
        member_id = esl.get_member_id_by_phone_number(members_list, phoneno)        
        task_result = esl.set_mode(show_name, member_id, mode)

        if task_result:           
            return True
        else:
            return False
            
    else:
        return False
    
def end_show(incoming_json):

    show_name = incoming_json['show_name']
    mongo.update_show_stats(show_name)
    
    if esl.end_conf(show_name):
        logger.info('success ending')
        return True
    else:
        logger.info('error ending')
        return False
