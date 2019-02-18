

import datetime
import redial_thread
import connectSQL
import sched
import time
import threading
import sys
from time import gmtime, strftime
from random import randint


try:
    import ESL
    import fs_config
except:
    print("Error Importing Custom Modules")
    print(traceback.print_exc())


con = ESL.ESLconnection(fs_config.server, fs_config.port, fs_config.password)
gateway = fs_config.gateway_doorvaani

if not con.connected:
    print('Not Connected')
    sys.exit(2)


#this file is to trigger actions at the Freeswitch side or server side


def launch_trailer(phone_number, show_id, cohort_id, file):
    x = randint(4, 20) #choosing random number of seconds to sleep for each trailer call thread
    time.sleep(x)
    folder_name  = "{folder="+file+"}"
    print("file received is ", file)

#    command = "originate " + folder_name + gateway + "+91" + phone_number + " 7777"
    command = "originate " + folder_name + "sofia/external/" + phone_number + "@" + fs_config.gateway_ip +  " 7777"
    print("[portal request handler] trailer esl command is ", str(command))
    print('freeswitch con value is '+str(con))
    action_command = con.api(str(command))
    result_str = str(action_command.getBody())
    print "command new is %s"+str(command)


    thread = redial_thread.Redial(show_id, show_id, cohort_id, phone_number, str(command), "trailer", "none")
    thread.start()

def schedule_trailer(date_str, time_str, phone_number, show_id, file):
    print "[portal request handler]\t received request for scheduling"
    print("scheduled time for the trailer is ", time_str)
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
    print("[portal request handler]Start a thread to run the events")
    t = threading.Thread(target=scheduler.run)
    t.start()
    return True


"""
def schedule_trailer(date_str, time_str, phone_number, show_id, file):

    print("file in portal reuest handler",file)
    value = esl.schedule_trailer(date_str, time_str, phone_number, show_id, file)
    return value
"""

