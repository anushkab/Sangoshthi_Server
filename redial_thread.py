'''
Created on Jun 24, 2016

@author: deepika-pc
'''
import sys
import threading
from threading import Thread

import ESL
import connectSQL
import fs_config as configuration
import json
#import esl_controller as esl
import time
import mongo_file as mongo
import broadcaster_publisher
import datetime


#mylock = threading.Lock()


def create_freeswitch_connection():
    freeswitch_connection = ESL.ESLconnection(configuration.server, configuration.port, configuration.password)
    if not freeswitch_connection.connected():
        print 'Not Connected'
        sys.exit(2)

    freeswitch_connection.events('plain', 'all')
    return freeswitch_connection



class Redial(Thread):
    
    def __init__(self, show_id, conference_name, cohort_id, phone_number, command, redial_case, parent_instance):
	self.phone_number = phone_number
        self.gateway = configuration.gateway_doorvaani
	self.gateway_ip = configuration.gateway_ip
        self._is_running = True
        self.show_id = show_id
	self.cohort_id = cohort_id
        self.redial_count = 0   
        self.command = command
        self.con = ""
        self.redial_case = redial_case
        self.conference_name = conference_name
        self.parent_instance = parent_instance
	   # self.redial_thread_dict = redial_thread_dict
        Thread.__init__(self)
            
    def stop(self):
	#if self.redial_case == "conference_start":
         #   mylock.acquire()
	 #   if self.redial_thread_dict[self.conference_name] == 0:
	 #       print("inform APPPP")
	 #       del self.redial_thread_dict[self.conference_name]
	 #   else:
#		print("reducing dictionary data")
#	        self.redial_thread_dict[self.conference_name] = self.redial_thread_dict[self.conference_name] - 1	
 #           print('length is ', len(self.show_thread_dict))
  #          mylock.release()

	self._is_running = False    

        
    def check_conf_live_status(self,conference_name):
        command = "conference list"
        result = ((self.con).api(command))
        value = str(result.getBody())

        if conference_name in value:
            return True
        else:
            return False



    def play_audio_conference(self,conference_name, file):
        print "going to play requested audio.."
        command = "conference " + conference_name + " play " + file
        result = (self.con).api(str(command))
        #value = str(result.getBody())
        if result:
            value = str(result.getBody())
            print("[Redial Thread]\t playing audio..." + value)
            return value
        else:
            print("[Redial Thread]freeswitch is down")
            return "none"


    def end_conference(self, conference_name):

        command = "conference " + conference_name + " kick all"
        result = (self.con).api(str(command))
        value = str(result.getBody())
        print("Body of end conference function: " + value)

        if "OK" in value:
            return True
        else:
            return False

     
    def run(self):
        self.con = create_freeswitch_connection()
        print('--- Redial Thread Started ---')
        total_listeners = connectSQL.get_listeners(self.cohort_id)
	#print("size of cohort is ", len(total_listeners))
	#print("redila case is", self.redial_case)

	#mylock.acquire()
	#self.redial_thread_dict[self.conference_name] = len(total_listeners)
	#mylock.acquire()

        while self._is_running:
            
            conference_event = (self.con).recvEvent()
            event_name = conference_event.getHeader("Event-Name", -1)
            
            if event_name == "CHANNEL_HANGUP" :
                
                if self.redial_count != 3:
                    if self.redial_case == "trailer":
                        print "Trailer Hangup"
                        cause = conference_event.getHeader("Hangup-Cause",-1)
                        hangup_number = conference_event.getHeader("Caller-Caller-ID-Number",-1)
                        if hangup_number:
                            hangup_number = hangup_number[len(hangup_number)-10:] #removing the locale
                            if str(hangup_number) == str(self.phone_number):
				print("calling "+ hangup_number+" again")
				#controller.insert_show_trailer_call_logs("listener_trailer_call_drop", self.show_id, self.cohort_id, hangup_number, self.redial_count)
                                

    				now = datetime.datetime.now()
			        now = now.strftime("%Y-%m-%d %H:%M:%S")

    				data = {'objective' : 'listener_trailer_call_drop',
            				'show_id' :  self.show_id,
            				'phone_number' : hangup_number,
            				'cohort_id' : self.cohort_id,
            				'call_attempt' : self.redial_count,
            				'timestamp' : now}

    				mongo.insert_show_trailer_call_logs(data)

				callresult = (self.con).api(self.command)
                                result_str = str(callresult.getBody())
                                print "redial thread, command in hangup case " + self.command
                                #log hangup event in the databaase
                                self.redial_count += 1
                    else:   
			#time gap between redialling, 8 seconds
                        time.sleep(8)
			#if not esl.check_conf_alive(self.conference_name):
			#    print('[redial] conference is destroyed, so closing the thread')
                        #    self._is_running = False
                        #    break;

			if not self.check_conf_live_status(self.conference_name):
                            print('[redial] conference is destroyed, so closing the thread')
                            self._is_running = False
                            break;

			print "Redial Conference Hangup"
                        cause = conference_event.getHeader("Hangup-Cause",-1)
                        hangup_number = conference_event.getHeader("Caller-Caller-ID-Number",-1)
                        if hangup_number:
                            hangup_number = hangup_number[len(hangup_number)-10:] #removing the locale
                            if str(hangup_number) == str(self.phone_number):
                        	time.sleep(1)
				if self.redial_case == "conference_start":

				    now = datetime.datetime.now()
    				    now = now.strftime("%Y-%m-%d %H:%M:%S")

    				    data = {'objective' : 'conference_start_drop',
            				'show_id' :  self.show_id,
            				'phone_number' : self.phone_number,
            				'cohort_id' : self.cohort_id,
            				'conference_name' : self.conference_name,
            				'call_attempt' : self.redial_count,
            				'timestamp' : now}

    				    mongo.insert_listener_show_call_logs(data)


  	                           #controller.insert_listener_conf_redial_call_logs("conference_start_drop", self.show_id, self.conference_name, self.phone_number, self.cohort_id, self.redial_count)
		
				if self.redial_case == "conference_redial":

                                    now = datetime.datetime.now()
                                    now = now.strftime("%Y-%m-%d %H:%M:%S")

                                    data = {'objective' : 'conference_redial_drop',
                                        'show_id' :  self.show_id,
                                        'phone_number' : self.phone_number,
                                        'cohort_id' : self.cohort_id,
                                        'conference_name' : self.conference_name,
                                        'call_attempt' : self.redial_count,
                                        'timestamp' : now}

                                    mongo.insert_listener_show_call_logs(data)
				    print("[Redial Thread], conference_redial_drop")
                                   #controller.insert_listener_conf_redial_call_logs("conference_redial_drop", self.show_id, self.conference_name, self.phone_number, self.cohort_id, self.redial_count)

				if self.redial_case == "conference_host_redial":

                                    now = datetime.datetime.now()
                                    now = now.strftime("%Y-%m-%d %H:%M:%S")

                                    data = {'objective' : 'conference_redial_host_drop',
                                        'show_id' :  self.show_id,
                                        'phone_number' : self.phone_number,
                                        'cohort_id' : self.cohort_id,
                                        'conference_name' : self.conference_name,
                                        'call_attempt' : self.redial_count,
                                        'timestamp' : now}

                                    mongo.insert_broadcaster_show_call_logs(data)
				    print("[Redial Thread], conference_redial_host_drop")

				    #controller.insert_broadcaster_show_call_logs("conference_redial_host_drop", self.show_id, self.conference_name, self.phone_number, self.cohort_id, self.redial_count)

				print("calling "+ hangup_number+" again")
			        callresult = (self.con).api(self.command)
                                result_str = str(callresult.getBody())
                                print "redial thread, command in hangup case " + self.command
                                #log hangup event in the databaase
                                self.redial_count += 1
                            
                else:
                    print('redial count timeout, stopping redial thread')
		    if self.redial_case == "conference_host_redial":
			print("host redial attempt finished, now kicking off the conference")
			
#			esl.play_audio_conference(self.conference_name, configuration.host_redial_timeout)#
#			time.sleep(20) 
#			esl.end_conference(self.conference_name)


                        self.play_audio_conference(self.conference_name, configuration.host_redial_timeout)
                        time.sleep(20)
                        result = self.end_conference(self.conference_name)
			self.parent_instance.stop()
			if not result :
				print('failed in firing the end conference command')

			broadcaster_no = connectSQL.get_broadcaster_from_cohortID(self.cohort_id)

			#data = {'objective': 'host_call_redial_timeout', 'conference_name': self.conference_name}
                        #json_data = json.dumps(data)
                        #broadcaster_publisher.send(json_data , broadcaster_no, "1")
			
			now = datetime.datetime.now()
			now = now.strftime("%Y-%m-%d %H:%M:%S")

			data = {'objective' :  'conference_end',
	            		    'show_id' : self.show_id,
        	    		    'conference_name' : self.conference_name,
           		 	    'cohort_id' : self.cohort_id,
            			    'timestamp' : now
            		          } 
			try:

				mongo.insert_freewitch_show_end_logs(data)
			except:
				print('exception in inserting conference end log when host redial timed out')

                        data = {'objective' : 'host_call_redial_timeout',
                                'show_id' :  self.show_id,
                                'phone_number' : self.phone_number,
                                'cohort_id' : self.cohort_id,
                                'conference_name' : self.conference_name,
                                'call_attempt' : self.redial_count,
                                'timestamp' : now}
			try:
                        	mongo.insert_broadcaster_show_call_logs(data)
			except:
				print('exception in inserting host_call_redial_timeout log when host redial time')
                        print("[Redial Thread], conference_redial_host_drop")


                    #self.update_db()#"no_response"
                    self._is_running = False
                   
            elif event_name == "CHANNEL_ANSWER":
                number = conference_event.getHeader("Caller-Caller-ID-Number",-1)
		print('[redial thread] channel ANSWER')
                if number:
                    number = number[len(number)-10:]
	            if str(number) == str(self.phone_number):                                          
			if self.redial_case == "conference_start": 
                            print('channel is answered by %s stopping redial thread',self.phone_number)
			    
                            now = datetime.datetime.now()
                            now = now.strftime("%Y-%m-%d %H:%M:%S")

                            data = {'objective' : 'conference_listener_start_answer',
                                    'show_id' :  self.show_id,
                                    'phone_number' : self.phone_number,
                                    'cohort_id' : self.cohort_id,
                                    'conference_name' : self.conference_name,
                                    'call_attempt' : self.redial_count,
                                    'timestamp' : now}

                            mongo.insert_listener_show_call_logs(data)
			    
			    print("[Redial Thread], conference_start_answer")

                            #controller.insert_listener_conf_redial_call_logs("conference_start_answer", self.show_id, self.conference_name, self.phone_number, self.cohort_id, self.redial_count)
                
                            print "exiting"
                            self._is_running = False

			if self.redial_case == "conference_redial":
                            print("[Redial Thread], conference_listener_redial_answer")
			    """
                            now = datetime.datetime.now()
                            now = now.strftime("%Y-%m-%d %H:%M:%S")

                            data = {'objective' : 'conference_redial_answer',
                                    'show_id' :  self.show_id,
                                    'phone_number' : self.phone_number,
                                    'cohort_id' : self.cohort_id,
                                    'conference_name' : self.conference_name,
                                    'call_attempt' : self.redial_count,
                                    'timestamp' : now}

                            mongo.insert_listener_show_call_logs(data)
			    """
                            
                           #controller.insert_listener_conf_redial_call_logs("conference_redial_answer", self.show_id, self.conference_name, self.phone_number, self.cohort_id, self.redial_count)

                            #print "exiting"
                            self._is_running = False
			
                        if self.redial_case == "conference_host_redial":
			    print("[Redial Thread], conference_redial_host_answer")
			    """

                            now = datetime.datetime.now()
                            now = now.strftime("%Y-%m-%d %H:%M:%S")

                            data = {'objective' : 'conference_redial_host_answer',
                                    'show_id' :  self.show_id,
                                    'phone_number' : self.phone_number,
                                    'cohort_id' : self.cohort_id,
                                    'conference_name' : self.conference_name,
                                    'call_attempt' : self.redial_count,
                                    'timestamp' : now}

                            mongo.insert_broadcaster_show_call_logs(data)
			    """
                            #controller.insert_broadcaster_show_call_logs("conference_redial_host_answer", self.show_id, self.conference_name, self.phone_number,self.cohort_id, self.redial_count)

			    self._is_running = False

			if self.redial_case == "trailer":

                            now = datetime.datetime.now()
                            now = now.strftime("%Y-%m-%d %H:%M:%S")

                            data = {'objective' : 'listener_trailer_call_answer',
                                    'show_id' :  self.show_id,
                                    'phone_number' : self.phone_number,
                                    'cohort_id' : self.cohort_id,
                                    'call_attempt' : self.redial_count,
                                    'timestamp' : now}

                            mongo.insert_show_trailer_call_logs(data)

                            #controller.insert_show_trailer_call_logs("listener_trailer_call_drop", self.show_id, self.phone_number, self.cohort_id, self.redial_count)

                            print "exiting"
                            self._is_running = False

                        
        print('[Redial Thread] Stopped')
                        
                
                

                    
