import datetime
import sched
import time
import threading
import sys
import thread
import traceback
import json
import redial_thread
import connectSQL
from time import gmtime, strftime

try:
    import ESL
    import fs_config
except:
    print("Error Importing Custom Modules")
    print(traceback.print_exc())

con = ESL.ESLconnection(fs_config.server, fs_config.port, fs_config.password)
gateway_doorvaani = fs_config.gateway_doorvaani

redial_thread_dict = {}


if not con.connected:
    print('Not Connected')
    sys.exit(2)
  
def add_broadcaster_to_conference(phone_number, locale, conference_name, flags, case, recording_file_path):
   
    recording_location = "{recordings_dir="+recording_file_path+"}"
  
    

    
    conference_dial_string = str("originate " +recording_location+
                                 gateway_doorvaani + locale +
                                 phone_number + 
                                 " &conference(" + conference_name + 
                                 "+flags{" + flags + "})")
    
#    conference_dial_string = str("originate " +recording_location+
#                                 "sofia/external/" +
#                                 phone_number + "@" + fs_config.gateway_ip +
#                                 " &conference(" + conference_name +
#                                 "+flags{" + flags + "})")
  


    
    print("Executing dial_string: " + conference_dial_string)
    
    result = con.api(conference_dial_string)
    if result:
    	value = str(result.getBody())
        print("Body of calling function: " + value)
    
        uuid = value[4:len(value)-1]   

        return value
    else:
	print("Freeswitch is down")
        return "none"
    #print("calling redial thread")
    #thread = redial_thread.Redial(conference_name,phone_number,conference_dial_string,case)
    #thread.start()



def record_listener_speaking(uuid, person_id, context, action):
    cmd_leg = str("uuid_setvar " + uuid + " RECORD_WRITE_ONLY true")
    set_write = con.api(cmd_leg)
    print "[eslcontroller]\t " + str(set_write.getBody())
    print "[eslcontroller]\t Set variable..."
    filename
    if action == 'start_record':
        command = str("uuid_record " + uuid + " start " + filename)
        action_command = con.api(str(command))
        print "[eslcontroller]\t Recording started..." + str(action_command.getBody())
    elif action == 'stop_record':
        command = str("uuid_record " + uuid + " stop " + filename)
        action_command = con.api(str(command))
        # media_manager.upload_file_cloudstudio(filename)
        print "[eslcontroller]\t Recording finished... " + str(action_command.getBody())



def add_listener_to_conference(phone_number, show_id, locale, conference_name, cohort_id, flags, case, recording_file_path, parent_thread_instance):


    recording_location = "{recordings_dir="+recording_file_path+"}"

    
    conference_dial_string = str("originate " + recording_location +
                                 gateway_doorvaani + locale +
                                 phone_number +
                                 " &conference(" + conference_name +
                                 "+flags{" + flags + "})")
    """

    conference_dial_string = str("originate " + recording_location +
                                 "sofia/external/" + phone_number + "@" + fs_config.gateway_ip +
                                 " &conference(" + conference_name +
                                 "+flags{" + flags + "})")
    """
    print("Executing dial_string: " + conference_dial_string)

    result = con.api(conference_dial_string)
    if result:
        value = str(result.getBody())
        print("Body of calling function: " + value)
	if value:
            uuid = value[4:len(value)-1]

        #print("calling redial thread")
            thread = redial_thread.Redial(show_id,conference_name,cohort_id,phone_number,conference_dial_string,case, parent_thread_instance)
            thread.start()
#	redial_thread_dict[conference_name] = redial_thread.Redial(show_id,conference_name,cohort_id,phone_number,conference_dial_string,case, redial_thread_dict)	
#	redial_thread_dict.start()
#        thread = redial_thread.Redial(show_id,conference_name,cohort_id,phone_number,conference_dial_string, case, redial_thread_dict)
#        thread.start()

            return value
	else:
	    print("freeswitch down")
	    return "none"
    else:
        print("freeswitch down")
        return "none"


def check_play_status(conference_name, file):
    command = 'conference ' + conference_name + ' play_status'
    result = con.api(str(command))

    if result:
        value = str(result.getBody())
	print("play status return is ", value)
        if file in value:
            return True
        else:
            return False

def get_play_status(conference_name):
    command = 'conference ' + conference_name + ' play_status'
    result = con.api(str(command))
    return str(result.getBody())



def pause_play_audio_conference(conference_name):
    command = 'conference ' + conference_name + ' pause_play'
    result = con.api(str(command))
    if result:
        value = str(result.getBody())
	print("return value of pause_play", value)
	if "OK" in value:
            return True
        else:
            return False



def get_conference_participants(conference_name):
    members = []
    e = con.api(str("conference " + conference_name + " list"))

    if e:
        result_body = e.getBody()
        #print("Body of get participants function: " + str(result_body))
        
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

def get_conference_participants_phone(conference_name):
    members = []
    e = con.api(str("conference " + conference_name + " list"))

    if e:
        result_body = e.getBody()
        
        if result_body is not None:
            results_list = result_body.splitlines()
            
            for line in results_list:
                results_list_parsed = line.split(';')

                try:
                    if len(results_list_parsed) > 4:
                        phone_number = results_list_parsed[4]
                        members.append(phone_number)                        
    
                except IndexError:
                    print("Range Error")
            return members
        
    print("No members found")
    return None


def play_audio_conference(conference_name, file):
    print "going to play requested audio.." 
    command = "conference " + conference_name + " play " + file
    result = con.api(str(command))
#    value = str(result.getBody())
    if result:
        value = str(result.getBody())
        print("[eslcontroller]\t playing audio..." + value)
        return value
    else:
        print("freeswitch is down")
        return "none"


def stop_audio_conference(conference_name):
    print "stopping conference playback media"
    command = "conference " + conference_name + " stop current"
    result = con.api(str(command))
    if result:
        print "[eslcontroller]\t playing audio..." + str(result)
        return result
    else:
        print("freeswitch is down")
        return "none"



def set_mode(conference_name, member, mode):
    print('[esl_controller]\tdetails are: ' + mode + " " + str(member) + " " + conference_name)
   
   #handle for None type member_id - Garima

    if mode == 'mute':
        command = 'conference ' + conference_name + ' mute ' + member
    elif mode == 'unmute':
        command = 'conference ' + conference_name + ' unmute ' + member

   # if mode == "mute":
   #     command = "conference " + conference_name + " mute " + member
   # elif mode == "unmute":
   #     command = "conference " + conference_name + " unmute " + member
        
    result = con.api(str(command))
    if result:
        value = str(result.getBody())
#    print("Body of muting function: " + value)
        print('[esl_controller]\tBody of Muting Function: ' + value)

        return True
    else:
        return False

def end_conference(conference_name):

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

   #exception handling- Garima

    for member in members_list:
        if member['phone_number'] == phone_number or member['phone_number'] == str("91" + phone_number):
            return member['member_id']
    return None


def get_conference_uuid(conference_name):
    command = "conference " + conference_name + " get uuid"
    result = con.api(str(command))
    value = str(result.getBody())
    print("Body of end conference function: " + value)
    return value

def conference_recording_action(file, conference_name, action):
    command = "conference "+ conference_name + " recording "+action + " "+file
    print("recording command", str(command))
    result = con.api(str(command))
    value = str(result.getBody()) 
    print("Body of end conference function: " + value)  

def launch_trailer(phone_number, show_id, cohort_id, file):
    time.sleep(3)
    folder_name  = "{folder="+file+"}"
    print("file received is ", file)

    command = "originate " + folder_name + gateway_doorvaani + "+91" + phone_number + " 7777"
#    command = "originate " + folder_name + "sofia/external/" + phone_number + "@" + fs_config.gateway_ip + " 7777"
    print("trailer esl command is ", str(command))
    action_command = con.api(str(command))
    result_str = str(action_command.getBody())
    print "command new is %s"+str(command)


    thread = redial_thread.Redial(show_id, show_id, cohort_id, phone_number, str(command), "trailer", "none")
    thread.start()


def schedule_trailer(date_str, time_str, phone_number, show_id, file):
    print "[eslcontroller]\t received request for scheduling"
    schedule_time = date_str+" "+time_str
    trailer_time = datetime.datetime.strptime(str(schedule_time), "%Y-%m-%d %H:%M:%S")
    cohort_id = connectSQL.get_cohortID_from_phoneno(phone_number)
    if cohort_id == "none" :
	cohort_id = connectSQL.get_cohortID_from_broadcasterno(phone_number)

    now = datetime.datetime.now()
    diff  = int((trailer_time - now).total_seconds())
    #epoch_format = time.mktime(trailer_time.timetuple())
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(diff, 1, launch_trailer, (phone_number, show_id, cohort_id, file))
    print("Start a thread to run the events")
    t = threading.Thread(target=scheduler.run)
    t.start()
    return True

