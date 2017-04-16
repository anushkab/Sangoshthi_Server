import datetime
import sched
import time
import threading
import re
import sys
import thread
import time
import traceback
from time import gmtime, strftime

try:
    import ESL
    import fs_config
except:
    print("Error Importing Custom Modules")
    print(traceback.print_exc())

con = ESL.ESLconnection(fs_config.server, fs_config.port, fs_config.password)
gateway = fs_config.gateway

if not con.connected:
    print('Not Connected')
    sys.exit(2)
  
def add_broadcaster_to_conference(phone_number, conference_name, flags, case):
   
    #recording_location = "{folder="+conference_name+"}"
    recording_location = ''
    conference_dial_string = str("originate " +recording_location+
                                 gateway + 
                                 phone_number + 
                                 " &conference(" + conference_name + 
                                 "+flags{" + flags + "})")
    
    print("Executing dial_string: " + conference_dial_string)
    
    result = con.api(conference_dial_string)
    value = str(result.getBody())

    print("Body of calling function: " + value)
    
    uuid = value[4:len(value)-1]    
    print('uuid ' , uuid)

    #print("calling redial thread")
    #thread = redial_thread.Redial(conference_name,phone_number,conference_dial_string,case)
    #thread.start()

def add_listener_to_conference(phone_number, conference_name, flags, case):
   
    #recording_location = "{folder="+conference_name+"}"
    recording_location = ''
    conference_dial_string = str("originate " +recording_location+
                                 gateway + 
                                 phone_number + 
                                 " &conference(" + conference_name + 
                                 "+flags{" + flags + "})")
    
    print("Executing dial_string: " + conference_dial_string)
    
    result = con.api(conference_dial_string)
    value = str(result.getBody())

    print("Body of calling function: " + value)
    
    uuid = value[4:len(value)-1]    
    print('uuid ' , uuid)
       
    #print("calling redial thread")
    #thread = redial_thread.Redial(conference_name,phone_number,conference_dial_string,case)
    #thread.start()

def get_conference_participants(conference_name):
    members = []
    e = con.api(str("conference " + conference_name + " list"))

    if e:
        result_body = e.getBody()
        print("Body of get participants function: " + str(result_body))
        
        if result_body is not None:
            results_list = result_body.splitlines()
            
            for line in results_list:
                results_list_parsed = line.split(';')

                try:
                    if len(results_list_parsed) > 4:
                        member_id = results_list_parsed[0]
                        uuid = results_list_parsed[2]
                        phone_number = results_list_parsed[4]
                        flags = results_list_parsed[5]
                        participant = {'member_id': member_id, 'uuid': uuid, 'phone_number': phone_number, 'flags': flags}
                        members.append(participant)
                        print("Member ID: " + member_id + "\t Caller Number: " + phone_number + "\t UUID: " + uuid + "\tFlags: " + flags)
                except IndexError:
                    print("Range Error")
            return members
        
    print("No members found")
    return None

def set_mode(conference_name, member, mode):

    if mode == "mute":
        command = "conference " + conference_name + " mute " + member
    elif mode == "unmute":
        command = "conference " + conference_name + " unmute " + member
        
    result = con.api(str(command))
    value = str(result.getBody())
    print("Body of muting function: " + value)
    return True

def end_conf(conference_name):

    command = "conference " + conference_name + " kick all"
    result = con.api(str(command))
    value = str(result.getBody())
    print("Body of end conference function: " + value)
    
    if "OK" in value:
        return True
    else:
        return False

def check_conf_alive(conference_name):
    command = "conference list"
    result = con.api(command)
    value = str(result.getBody())
    
    if conference_name in value:
        return True
    else:
        return False

def get_member_id_by_phone_number(members_list, phone_number):
    for member in members_list:
        if member['phone_number'] == phone_number:
            return member['member_id']
    return None

