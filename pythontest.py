#!/usr/bin/python

import os, sys
import connectSQL
import esl_controller as esl
import controller as ctrl
import datetime
import time
import sched
import esl_controller as esl
import threading
import re
import sys
import thread
#import time
import traceback
import mongo_file as mongo
import pytz

#import portal_request_handler as portal


"""
# Path to be created
path = "/home/sangoshthi/sangoshthi_new/dir"

os.mkdir( path, 0755 );

print "Path is created"


phone = "9716517818"

def get_cohortID_from_phoneno(phone):

    query1 = 'select WebPortal_cohort_listeners.cohort_id from WebPortal_cohort_listeners INNER JOIN WebPortal_asha ON ' \
             'WebPortal_cohort_listeners.asha_id = WebPortal_asha.id where WebPortal_asha.phoneNumber =\''+phone+'\''

    print(query1)


listeners = connectSQL.get_listeners("3")
print(listeners)
for listener in listeners:
    print("calling listener with phone number",str(listener[0]))
    esl.add_listener_to_conference(str(listener[0]), "91", "123", "mute","conference")



#print(connectSQL.get_cohortID_from_phoneno("8377846695"))
cohort_id = "3"
query1 = 'select showID, timeOfAiring from WebPortal_show where cohort_id = \'' + cohort_id + '\' and status = \'0\''
print(query1)
try:
    cursor.execute(query1)
    data = cursor.fetchall()
    print(dta)
except:
    print "exception in listeners numbers"
    return "none"


def launch_trailer(arg,arg2):
    print("hello",arg,arg2)

def print_time(a='default'):
    print("From print_time", time.time(), a)


trailer_time = datetime.datetime.strptime("2017-06-03 10:17:00", "%Y-%m-%d %H:%M:%S")
now = datetime.datetime.now()
#now_time  = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S" )

diff  = int((trailer_time - now).total_seconds())

#trailer_time = "2017-06-02" "20:35:00"
sec = time.mktime(trailer_time.timetuple())
scheduler = sched.scheduler(time.time, time.sleep)
#scheduler.enter(2, 1, launch_trailer, ("hello"))
scheduler.enter(diff, 1, launch_trailer, ("sdf","123"))
print("Start a thread to run the events")

t = threading.Thread(target=scheduler.run)
t.start()
print "-----hey"

#scheduler = sched.scheduler(time.time, time.sleep)
#status = esl.schedule_trailer("2017-06-03", "00:27:00", "9958691307","1", "/usr/local/freeswitch/sounds/music/testingfiles/ChillingMusic.wav")


list1 = []
list1.append("9871273")
list1.append('def')
print(list1)
if str(9871273) in list1:
    print("exists")

list1.remove('abc')

if not 'abc' in list1:
    print("not exists")


print(list1)


status = connectSQL.get_content_for_show("show_2")
print(status)


#cohort_id = "2"
#if cohort_id != "none":
#    print "match not"




listeners = connectSQL.get_listeners('1')
print(str(listeners[0]))

list1 = []
for listener in listeners:
    print("calling listener with phone number",str(listener[0]))
    list1.append(str(listener[0]))      


if "8377843489" in list1:
    print ":P"


#id =  connectSQL.get_cohortID_from_phoneno('8377846695')
#print("found",id)



dict1 = {}
dict1['123'] = 'no'
print('dict1',dict1)


arraytest = myList=[0 for i in range(10)]
arraytest[0] = "fds"
arraytest[1] = 'sfdfds'



status = ctrl.call_conference_host("1234","abc", "/")


def update_show_status(data):
    show_id = data['show_id']
    status = data['sattus']
    ret_value = connectSQL.update_show_status(show_id, status)
    if ret_value == 'ok':
        return True
    else:
        return False


val = connectSQL.update_show_status('show_1', '1')
print(val)


test = []
test.append('123')
print(test)
test.remove('123')


data = {'phone_number': '9716517818',\
        'show_id': u'show_1', \
        'cohort_id': u'1', \
        'timestamp': '2017-06-10 16:46:11', \
        'conference_name': u'show_1_2017_06_10_16_43_12', \
        'objective': 'conference_listener_test_call_drop', 
        }


val= mongo.insert_listener_show_call_logs(data)
print(val)


val = esl.play_audio_conference("show_1_2017_06_12_11_38_31", "/home/sangoshthi/sangoshthi_new/sounds/wait_for_host.wav")
val = ctrl.get_cohort_size("1")


id = connectSQL.get_cohortID_from_phoneno('9716517818')
print(id)


msg_list = mongo.get_notifications("9425592627")
print(str(msg_list))

phone = '123'
body = 'fe'
msg_id = '1234445'


#new_data = "{ phoneno :" + phone+", data : [{msg_id : " +msg_id + ", body : " + body + ", read_status : 0 }]"
new_data = { 'phoneno' : phone, 'data' : [ {'msg_id' : msg_id, 'body' : body , 'read_status' : '0' }]}


print(new_data)

mongo.insert_user_notifications("202", "next upcoming program is ready , you should now listen to its content and prepare well", ['8368861819',])
#mongo.update_user_notifications("202", "2377777")


value = connectSQL.get_feedback_for_show("show_6")
print(value)

def convert_utc_ist(time_string):
    print("time string received", time_string)
    utc_time = datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')
    print(str(utc_time))
    local_tz = pytz.timezone('Asia/Kolkata')
    utc_time = pytz.utc.localize(utc_time) #converting utc time object to utc timezone
    local_time = utc_time.astimezone(local_tz) # converting utc to local Asia/ist timezone
    print("the local time is", str(local_time))
    parsed_time_string  = str(local_time).split('+')
    print(parsed_time_string[0])
    return parsed_time_string[0]


time_val = connectSQL.get_upcoming_show_time("1")
print(time_val)

val = convert_utc_ist(time_val)
print(val)

value = portal.schedule_trailer('2017-06-21', '11:29:10', '9716517818', 'show_1', '/home/sangoshthi/sangoshthi_new/sounds/wait_for_host.wav')
print(value)

val = connectSQL.get_upcoming_showID('1')
print(val)


val = mongo.get_notifications('9716517818')
print(val)


val = mongo.insert_user_notifications("10002", "te4sting", ["9716517818", "123"])
print(val)

map = connectSQL.get_cohort_members_name_phone_mapping('1')
for member in map:
	print(member[0])
"""

ctrl.get_active_participants_phone('show_16_2017_07_27_23_42_26')
