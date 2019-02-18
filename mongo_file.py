from flask import Flask
from flask_pymongo import PyMongo
import json
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'sangoshthi_audio'
#app.config['MONGO_URI'] = 'mongodb://192.168.2.71:27017/sangoshthi_audio'
app.config['MONGO_URI'] = 'mongodb://0.0.0.0:27017/sangoshthi_audio'

mongo = PyMongo(app)

# NETWORK COMMANDS

# create a new show

def insert_show_stats(data):

    with app.app_context():
        entries = mongo.db.show_list
        status = entries.insert(data)
        print(data)
        return status

def insert_user_notifications(msg_id, body, recipient_list, timestamp):
    with app.app_context():
	try:
	    status = mongo.db.notification_user_mapping.update({"msg_id" : msg_id}, {"$set": {"body" : body, "recipient_list" : recipient_list, 'timestamp' : timestamp}},  upsert=True)
	    return status
	except:
	    print "exception"
	    return "none"


def insert_broadcaster_content_listen_data(data):
    with app.app_context():
	entries = mongo.db.broadcaster_content_listen_logs
        status = entries.insert(data)
        return status
		

def update_user_notifications(msg_id, recipient_list):
    with app.app_context():
	for recipient in recipient_list:
	    mongo.db.notification_user_mapping.update({"msg_id": msg_id }, {"$addToSet": {"recipient_list": recipient}})	    


def insert_show_trailer_call_logs(data):
    with app.app_context():
        entries = mongo.db.show_trailer_call_logs
        status = entries.insert(data)
        print(data)
        return status

def insert_portal_created_show_data(data):

    with app.app_context():
        entries = mongo.db.portal_created_shows
        status = entries.insert
        return status


def insert_app_install_data(data):

    with app.app_context():
        entries = mongo.db.app_install
        status = entries.insert(data)
        return status



def insert_show_conference_timestamps(data):

    with app.app_context():
        entries = mongo.db.show_conference_timestamps
        status = entries.insert(data)
        return status






def get_poll_results(showid , pollid):
    with app.app_context():	
	entries = mongo.db.user_polling_logs

        output = []
        nowDate= datetime.now() 

        for q in entries.find():
	    print ('in entries')
            if(str(q['show_id']) == str(show_id) and str(q['poll_id']) == str(pollid) and q['action'] == 'valid key'):
                output.append({'show_id' : q['show_id'] ,
                                   'server_timestamp' : nowDate ,
                                   'poll_id' : q['poll_id'] ,
                                   'phone_no' : q['phone_no'],
                                   'digit_pressed' : q['digit_pressed']})

        return output


def insert_user_mute_unmute_freeswitch_logs(data):
    with app.app_context():
	try:
            entries = mongo.db.user_mute_unmute_freeswitch_logs
            status = entries.insert(data)
            #print(data)
	except:
	    print("error in inserting mute unmute logs in mongodb ")

def insert_user_speak_freeswitch_logs(data):
    with app.app_context():
	try:
            entries = mongo.db.user_speak_freeswitch_logs
            status = entries.insert(data)
	except:
	    print("error in inserting speak logs in mongodb")
        #print(data)

def insert_user_polling_logs(data):
    with app.app_context():
        entries = mongo.db.user_polling_logs
        status = entries.insert(data)
        print(data)

def insert_listeners_conference_dtmf_events(data):
    with app.app_context():
	try:
            entries = mongo.db.listeners_conference_dtmf_events
            status = entries.insert(data)
            #print(data)
	except:
	    print("error in inserting conference dtmf logs in mongodb")

def insert_show_polling_logs(data):
    with app.app_context():
        entries = mongo.db.show_polling_logs
        status = entries.insert(data)
        #print(data)


def get_matching_broadcasters(phone_no):

    with app.app_context():
        entries = mongo.db.show_list

        output = []
        nowDate= datetime.now() - timedelta(minutes = 90)
        DateNow = nowDate.strftime('%Y-%m-%d %H:%M:%S')
        DatePresent = datetime.strptime(DateNow, '%Y-%m-%d %H:%M:%S')
        
        for q in entries.find():
            
            inDate = q['time_of_airing']
            DateIn = datetime.strptime(inDate, '%d/%m/%Y %H:%M:%S')
            listAsha = []
            
            if(DateIn > DatePresent):
		print (q['broadcaster_phoneno'] , str(phone_no))
                if(str(q['broadcaster_phoneno']) == str(phone_no)):
                    output.append({'show_id' : q['show_id'] ,
                                   'timestamp' : q['timestamp'] ,
                                   'list_of_listeners' : q['list_of_listeners'] ,
                                   'audio_name' : q['audio_name'],
                                   'time_of_airing' : q['time_of_airing']})

        return output


def get_msg_body_by_id(msg_id):
    with app.app_context():
        entries  =   mongo.db.notification_pool
        for q in entries.find():
            for q1 in q['data']:
                if q1['msg_id'] == msg_id:
                    return q1['body']

def check_user_notification_status(msg_id,phoneno):
    print(msg_id,phoneno)
    with app.app_context():
        entries  =   mongo.db.user_notification_status
	try:
            for q3 in entries.find():
                if q3['phoneno'] == phoneno:
               # print("user notification data is "+json.dumps(q3['data']))
                    for entry in q3['data']:
                        if entry['msg_id'] == 'msg_id':
                       # print("present exiting")
                            return "found"
                        else:
                            continue

            return "not found"
	except:
	    return "none"



def update_notification(msg_id,body, phone, timestamp):
    #print("update notification function", phone, ", ", body, ", ", msg_id)
    with app.app_context():
        entries  =   mongo.db.user_notification_status
	try:
        

#            for q in entries.find():
#                    if q['phoneno'] == phone:
#  		        print("previous notification data exists , so updating it")
            status = entries.update({"phoneno": phone }, {"$addToSet":{"data":{"msg_id" : msg_id, "body" : body, "read_status" : "0", "timestamp": timestamp}}}, upsert=True)

#	        print("no notifications for this user, now adding")
#	        new_data = { 'phoneno' : phone, 'data' : [ {'msg_id' : msg_id, 'body' : body , 'read_status' : '0' }]}
	      
	            #print(new_data)
#	        status = entries.insert(new_data)

#                    mongo.db.user_notification_status.insert(new_data)
#	    print("out of find loop")
	except:
	    print("exception occured in updating user_notification_status called from get_notification")



def get_user_notification_list(phoneno):
    notification_list ="none"
    with app.app_context():
        entries  =   mongo.db.user_notification_status
        for q in entries.find():
            if q['phoneno'] == phoneno:
                notification_list = q['data']
        return notification_list




def get_notifications(phoneno):

    with app.app_context():
        entries  =   mongo.db.notification_user_mapping
        found_flag = 0


	for q in entries.find():
	    try:
	        if any(phoneno in s for s in q['recipient_list']):

                    msg_status = check_user_notification_status(q['msg_id'],phoneno)
		    #print("messge status for the useer", msg_status)
                    if msg_status == "not found":
			#print("message not found")
		        body = q['body']
			timestamp = q['timestamp']
		        #print("now the body of the mesg to be sent is ", q['body'])
                        update_notification(q['msg_id'],body,phoneno,timestamp)

                        found_flag = 1

                    else:

                        continue
	    except:
		print("exception in fetching notification data")
		return "none"
	    
        return get_user_notification_list(phoneno)

# play/pause commands
def insert_play_pause_stats(data):

     with app.app_context():
	try:
            entries = mongo.db.show_media_playback_logs
            status = entries.insert(data)
            print(data)
            return status
	except:
	    print("exception in logging media playback data")
	    return "none"

# flush query
def insert_QA_round_flush(data):

     with app.app_context():
	
        entries = mongo.db.show_QA_timestamps
        status = entries.insert(data)
        #print(data)
        return status
    
# asha has raised a query
def insert_asha_query_stats(data):

    with app.app_context():
        entries = mongo.db.asha_dtmf_logs
        status = entries.insert(data)
        #print(data)
        return status
        
# asha liked the video
def insert_asha_like_stats(data):

    with app.app_context():
        entries = mongo.db.asha_like_logs
        status = entries.insert(data)
        print(data)
        return status

# get show status if finished or not, if finished then return 0 else 1
def get_show_status(show_name):
    
    with app.app_context():
        entries = mongo.db.show_list
        
        for q in entries.find():
            if(q['show_id'] == show_name):
                return q['show_hosting_status']

        return 0

# FREESWITCH COMMANDS

# schedule the broadcast of trailer
def insert_spread_word_stats(data):

    with app.app_context():
        entries = mongo.db.show_trailer_logs
        entries.insert(data)
        print(data)

# add delete listener stats
def insert_del_listener_stats(data):

    with app.app_context():
        entries = mongo.db.del_listener_stats
        status = entries.insert(data)
        print(data)
        return status
        
# delete listener from show_stats table
def del_listener(show_name , phone):
    
    with app.app_context():
        entries = mongo.db.show_list       
        status = entries.update({"show_id":show_name},{"$pull" : {"list_of_listeners" : phone}})
        return status

# add delete all listeners stats
def insert_del_all_listener_stats(data):

    with app.app_context():
        entries = mongo.db.del_all_listener_stats
        status = entries.insert(data)
        print(data)
        return status

# delete all listeners from show_stats table     
def del_all_listener(show_name):
    
    with app.app_context():
        entries = mongo.db.show_list
        status = entries.update({"show_id":show_name},{"$set" : {"list_of_listeners" : []}})
        return status

# add play trailer stats
def insert_play_trailer_stats(data):

     with app.app_context():
        entries = mongo.db.play_trailer_stats
        status = entries.insert(data)
        print(data)
        return status

# add delete trailer stats
def insert_delete_trailer_stats(data):

    with app.app_context():
        entries = mongo.db.delete_trailer_stats
        status = entries.insert(data)
        print(data)
        return status

# add call broadcaster stats
def insert_broadcaster_show_call_logs(data):
    with app.app_context():
        entries = mongo.db.broadcaster_show_call_logs
        status = entries.insert(data)
        print(data)
        return status
    
# get broadcaster for a specific show
def get_broadcaster_from_db(show_name):

    with app.app_context():
        entries = mongo.db.show_list
        
        for q in entries.find():
            if(q['show_id'] == show_name):
                return q['broadcaster_phoneno']

        return 0

# add call listener stats
def insert_listener_show_call_logs(data):
    with app.app_context():
        entries = mongo.db.listener_show_call_logs
        status = entries.insert(data)
        print(status)
        return status


def insert_broadcaster_show_call_logs(data):
    with app.app_context():
        entries = mongo.db.broadcaster_show_call_logs
        status = entries.insert(data)
        print(data)
        return status

    
# get ashas for a specific show
def get_ashas_from_db(show_name):

    with app.app_context():
        entries = mongo.db.show_list
        
        for q in entries.find():
            if(q['show_id'] == show_name):
                return q['list_of_listeners']

        return 0

# add mute/unmute stats
def insert_mute_unmute_logs(data):

    with app.app_context():
        entries = mongo.db.user_mute_unmute_app_logs
        status = entries.insert(data)
        print(data)
        return status

# update show stats flag when show ends
def update_show_stats(show_name):

    with app.app_context():
        entries = mongo.db.show_list   
	try:

            status = entries.update({"show_id":show_name},{"$set" : {"show_hosting_status" : '0'}})
            return status
	except:
	    print("exception in updating show status")
	    return "none"

# get show status
def get_show_status(show_name):

    with app.app_context():
        entries = mongo.db.show_list        

        for q in entries.find():
            if(q['show_id'] == show_name):
                return q['show_id']
            
        return 0


def insert_freewitch_show_end_logs(data):
    with app.app_context():
        entries = mongo.db.freeswitch_end_show_logs
        status = entries.insert(data)
        return status



def insert_app_end_show_logs(data):
    with app.app_context():
	try:
            entries = mongo.db.app_end_show_logs
            status = entries.insert(data)
            return status
	except:
	    print("exception in logging end show ")
	    return "none"

