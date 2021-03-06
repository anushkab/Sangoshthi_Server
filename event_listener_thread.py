import traceback, sys
import broadcaster_publisher
#import broadcaster_publisher
import controller
import datetime
import connectSQL
import fs_config as config
import threading
import mongo_file as mongo
import time
#import broadcaster_request_handler
    
try:
    import ESL
    import esl_controller as esl
    import threading
    import json
    from threading import Thread
    #from datetime import datetime
    
except:
    print("Error importing custom modules")
    print(traceback.print_exc())

global count_1,count_2,count_3,count_4, start_polling, stop_polling, polling_start_time, polling_stop_time
count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0

start_polling = False
stop_polling = False
options = 0
poll_id = 0

polling_start_time = ""
polling_stop_time = ""

polling_member_list = []
#dtmf_1_member_list = []
#conference_connected_listeners  = []

#cohort_members = []
#exceed_attempt_range_attemptee_list = []
#connected_callers_list = []


mylock = threading.Lock()

def create_freeswitch_connection():
    freeswitch_connection = ESL.ESLconnection(config.server, config.port, config.password)
    if not freeswitch_connection.connected():
        print('Not Connected')
        sys.exit(2)
    freeswitch_connection.events('plain', 'all')
    #freeswitch_connection.events('plain', 'BACKGROUND_JOB')
    return freeswitch_connection
	
		
class EventListenerThread(Thread):

    def __init__(self, show_id, cohort_id, conference_name, broadcaster_no, show_thread_dict):
        self.show_id = show_id
        self._is_running = True
        #self.callers_count = 0
        self.cohort_id = cohort_id
        self.conference_name = conference_name
        self.broadcaster_no = broadcaster_no
        self.dtmf_1_member_list = []
        self.conference_connected_listeners = []
        self.cohort_members = []
        self.QA = 1
	self.show_thread_dict = show_thread_dict
	self.current_media_jobUUID = ""
	self.playback_flag = "none"
	self.playback_orderno = "-1"
	self.dial_listeners_flag = 0
        self.conf_recording_path = ""

        Thread.__init__(self)

    def flush_dtmf_members_list(self):

        print('received request to flush dtmf member list, cohort id ', self.cohort_id)
        del self.dtmf_1_member_list[:]
	self.QA += 1

    def QA_recording_action(self,phone_number, action, turn):
	base_recording_dir = config.recording_dir + self.show_id + "/" + self.conference_name+ "/" + str(self.QA)+"/"+phone_number+"_"+str(turn)+".wav"
	esl.conference_recording_action(str(base_recording_dir),self.conference_name,  action)
 
    def set_playback_flag(self, case, orderno):
	self.playback_flag = case
	self.playback_orderno = orderno
#	print("playback flag"+str(self.playback_flag))

    def set_dial_listeners_flag(self):
	self.dial_listeners_flag = 1


    def set_conf_recording_path(self, path):
	self.conf_recording_path = path
	
    def stop(self):
        #esl.conference_recording_action(self.show_id, self.conference_name, "stop")
#        del mainthread.show_thread_dict[self.broadcaster_no]
	print("[event listener cohort - "+ self.cohort_id+"] removing my thread object from the dictionary")
	if self.broadcaster_no in self.show_thread_dict.keys():
	    #print('length is ', len(self.show_thread_dict))
	
	    mylock.acquire()
            del self.show_thread_dict[self.broadcaster_no]
	    #print('length is ', len(self.show_thread_dict))
	    mylock.release()
	

        data = {"objective" : "end_show_call_ack", "info" : "OK"}
        json_data = json.dumps(data)
        broadcaster_publisher.send(json_data , self.broadcaster_no, "1")


        self._is_running = False



    #take action when a call in a conference is answered
    def handle_channel_answer(self,conference_event):
        phone_number = conference_event.getHeader("Caller-Caller-ID-Number", -1);

        if phone_number:
            phone_number = phone_number[len(phone_number)-10:] #removing the locale
	    if phone_number in self.cohort_members:
                #print("My turn ,  cohort  no", self.cohort_id)

	        #adding to the conference connected listeners list
		self.conference_connected_listeners.append(phone_number)
                #print("connected listeners are ", self.conference_connected_listeners)

		name = connectSQL.get_use_name(phone_number)

		#if name != 'none':
		#	data = {'objective' : 'conf_member_status', 'show_id' : self.show_id,'conference_name': self.conference_name, 'phoneno' : name , 'task' : 'online'}
		#else:
		data = {'objective' : 'conf_member_status', 'show_id' : self.show_id,'conference_name': self.conference_name, 'phoneno' : phone_number , 'task' : 'online'}
                
		json_data = json.dumps(data)
                broadcaster_publisher.send(json_data , self.broadcaster_no, "2")
  
		


		controller.insert_listener_show_call_logs("conference_listener_call_answer", self.show_id, self.conference_name, phone_number, self.cohort_id)



	    elif phone_number == self.broadcaster_no:
                #print("broadcaster number",  self.cohort_id)
		self.conference_connected_listeners.append(phone_number)
		#print("HOST ANSWER adding into the list", str(self.conference_connected_listeners))
                controller.insert_broadcaster_show_call_logs("conference_host_call_answer", self.show_id, self.conference_name, phone_number, self.cohort_id, "none")

              
            #else:
	        #print("Not Mine, cohort  no", self.cohort_id)
            
        else:
            print("[event listener cohort - "+ self.cohort_id+"] no phone number captured")

    def handle_mute_unmute(self, conference_event, action):
 
        phone_number = conference_event.getHeader("Caller-Caller-ID-Number", -1);
        
        if phone_number:

            phone_number = phone_number[len(phone_number)-10:]
	    if phone_number in self.cohort_members:
	        if action == "unmute-member":
#	            data = {'objective' : 'mute_unmute_result', 'body' : 'OK', }
                    data = {'objective': 'mute_unmute_response', 'info': 'OK', 'listener_phoneno': phone_number}	 
	            json_data = json.dumps(data)
        	    broadcaster_publisher.send(json_data , self.broadcaster_no, "1")

   		    if phone_number in self.dtmf_1_member_list:

         	        controller.freeswitch_conf_mute_unmute_logging(self.show_id,self.conference_name, self.cohort_id, phone_number, "unmute", "yes")
		    else:
                        controller.freeswitch_conf_mute_unmute_logging(self.show_id,self.conference_name, self.cohort_id, phone_number, "unmute", "no")

		elif action == "mute-member": 
		    if phone_number in self.dtmf_1_member_list:
			self.dtmf_1_member_list.remove(phone_number)
                        data = {'objective': 'mute_unmute_response', 'info': 'OK', 'listener_phoneno': phone_number}
                        json_data = json.dumps(data)
                        broadcaster_publisher.send(json_data , self.broadcaster_no, "1")
                        controller.freeswitch_conf_mute_unmute_logging(self.show_id,self.conference_name, self.cohort_id, phone_number, "mute", "yes")
		    else:

			data = {'objective': 'mute_unmute_response', 'info': 'OK', 'listener_phoneno': phone_number}
                        json_data = json.dumps(data)
                        broadcaster_publisher.send(json_data , self.broadcaster_no, "1")
             		controller.freeswitch_conf_mute_unmute_logging(self.show_id,self.conference_name, self.cohort_id, phone_number, "mute", "no")

       
            

    def handle_speak_events(self, conference_event, event):
        phone_number = conference_event.getHeader("Caller-Caller-ID-Number", -1);
	if phone_number:
            phone_number = phone_number[len(phone_number)-10:]
	    if phone_number in self.cohort_members:
#	  	print("person with phone number  "+str(phone_number)+" spoke")
		#print("start-talking event of my thread, person ", phone_number)
        	controller.freeswitch_conf_speak_event_logging(event, self.show_id, self.conference_name, self.cohort_id, phone_number)
	    elif phone_number == self.broadcaster_no:
		#print("start-talking event of my thread, person ", phone_number)
		controller.freeswitch_conf_speak_event_logging(event, self.show_id, self.conference_name, self.cohort_id, phone_number)
 
 
    #handle key press event by the listenere during an on-going conference call
    def handle_key_press(self,conference_event):
        digit_pressed = conference_event.getHeader("DTMF-Digit", -1);
        #uuid = conference_event.getHeader("Caller-Unique-ID", -1);
        phone_number = conference_event.getHeader("Caller-Caller-ID-Number", -1);
#        phone_number = phone_number[len(phone_number)-10:] #removing the locale

        #log key pressed and its timestamp to database - Garima

        global polling_member_list, start_polling, stop_polling, polling_start_time, polling_stop_time, count_choice, count_1, count_2, count_3, count_4            

        if phone_number:
	    phone_number = phone_number[len(phone_number)-10:]
            if phone_number in self.cohort_members:
            #if connectSQL.get_cohortID_from_phoneno(phone_number) == self.cohort_id:

                #check if dtmf is for query or quiz/polling activity
                if start_polling == True :
            
                    print('....Polling started....')
                  
                    if not phone_number in polling_member_list:                          
                        if digit_pressed == '1':
                            count_1 = count_1 + 1
                            print('count_1 after assignment is %s',str(count_1))
                            polling_member_list.append(phone_number)
                        #log into database - Garima

		            data = {'objective' : 'get_polling_result_response', 
				'show_id' : self.show_id, 
				'phoneno' : phone_number , 
				'poll_id' : poll_id , 
				'response' : digit_pressed}

                            json_data = json.dumps(data) 
                            print('[event_listener_thread]\t Listener press 1 event: ' + str(json_data))

                        #broadcaster_publisher.send(json_data)
                            broadcaster_no = controller.get_broadcaster(self.show_id)
                            broadcaster_publisher.send(json_data , broadcaster_no, "1")

		            controller.polling(self.show_id , phone_number , digit_pressed , poll_id , 'valid key')

                        elif digit_pressed == '2':
                            count_2 = count_2 + 1
                            print('count_2 after assignment is %s',str(count_2))
                            polling_member_list.append(phone_number)
                        #log into database - Garima

                            data = {'objective' : 'get_polling_result_response',
                                'show_id' : self.show_id,
                                'phoneno' : phone_number ,
                                'poll_id' : poll_id ,
                                'response' : digit_pressed}
                            json_data = json.dumps(data)
                            print('[event_listener_thread]\t Listener press 1 event: ' + str(json_data))

                        #broadcaster_publisher.send(json_data)
                            broadcaster_no = controller.get_broadcaster(self.show_id)
                            broadcaster_publisher.send(json_data , broadcaster_no, "1")

		            controller.polling(self.show_id , phone_number , digit_pressed , poll_id , 'valid key')

       	                elif digit_pressed == '3':
		     
		            if options == '4' or options == '3':
                    	        count_3 = count_3 + 1
                    	        polling_member_list.append(phone_number)
                    	    #logging the event into database 
		    	        controller.polling(self.show_id , phone_number , digit_pressed ,poll_id , 'valid key')
                    
                                data = {'objective' : 'get_polling_result_response',
                                'show_id' : self.show_id,
                                'phoneno' : phone_number ,
                                'poll_id' : poll_id ,
                                'response' : digit_pressed}
                                json_data = json.dumps(data)
                                print('[event_listener_thread]\t Listener press 1 event: ' + str(json_data))

                            #broadcaster_publisher.send(json_data)
	                        broadcaster_no = controller.get_broadcaster(self.show_id)
        	                broadcaster_publisher.send(json_data , broadcaster_no, "1")

			    elif options == '2':
		                logger.info('invalid digit pressed')
                                #logging the event into database
                                controller.polling(self.show_id ,phone_number , digit_pressed ,poll_id , 'invalid key')


                        elif digit_pressed == '4':

		            if options == '4':
                                count_4 = count_4 + 1
                    	        polling_member_list.append(phone_number)
                    	#logging the event into database

                    	        controller.polling(self.show_id , phone_number , digit_pressed ,poll_id , 'valid key')
		    
                                data = {'objective' : 'get_polling_result_response',
                                'show_id' : self.show_id,
                                'phoneno' : phone_number ,
                                'poll_id' : poll_id ,
                                'response' : digit_pressed}
                                json_data = json.dumps(data)
                                print('[event_listener_thread]\t Listener press 1 event: ' + str(json_data))

                        #broadcaster_publisher.send(json_data)
                                broadcaster_no = controller.get_broadcaster(self.show_id)
                                broadcaster_publisher.send(json_data , broadcaster_no, "1")

		            elif options == '3' or options == '2':
			        logger.info('invalid digit pressed')
                                #logging the event into database
                                controller.polling(self.show_id ,phone_number , digit_pressed , poll_id ,'invalid key')
 
                        else:
                            logger.info('invalid digit pressed')
                            #logging the event into database
		            controller.polling(self.show_id ,phone_number , digit_pressed , poll_id ,'invalid key')

                    #invalid_entry_attemptee_list.append(phone_number)
                    #todo play sound to the user

             #sending polling responses to broadcaster - Garima
                


                    else:
                        print('person attempting again not allowed')
		        controller.polling(self.show_id ,phone_number , digit_pressed ,poll_id , 'invalid attempt')

                else:
                    if digit_pressed == '1':
                        print("[event listener cohort - "+ self.cohort_id+"] \n---1 pressed!\n")
                        if not phone_number in self.dtmf_1_member_list:
            
                            #sending connected callers count to the broadcaster
                            data = {'objective' : 'press_1_event', 'show_id' : self.show_id, 'conference_name': self.conference_name, 'phoneno' : phone_number}
                            json_data = json.dumps(data)
#                            print('[event_listener_thread]\t Listener press 1 event: ' + str(json_data))
                            broadcaster_publisher.send(json_data , self.broadcaster_no, "1")           
                    
                            #adding to the cache of listenere who did press 1 event      
                            self.dtmf_1_member_list.append(phone_number)
            
                            #adding to the database
         	            controller.insert_listeners_conference_dtmf_events("conference_listener_dtmf", self.show_id, self.conference_name , self.cohort_id, phone_number, digit_pressed , 'valid key')
  
                        else:
			    print('dtmf list is ', str(self.dtmf_1_member_list))
                            print("[event listener cohort - "+ self.cohort_id+"] listener press 1 again in the same QA")
                            controller.insert_listeners_conference_dtmf_events("conference_listener_dtmf", self.show_id, self.conference_name, self.cohort_id, phone_number, digit_pressed, 'invalid attempt')

                    else:
		        print ('invalid key')
		        controller.insert_listeners_conference_dtmf_events("conference_listener_dtmf", self.show_id, self.conference_name ,self.cohort_id, phone_number, digit_pressed, 'invalid key')


                    #log the event into database - Garima
 
    
    def handle_conference_end(self,conference_event):
        #conference_uuid = esl.get_conference_uuid(self.conference_name)
        print("[event listener cohort - "+ self.cohort_id+"], on conference destroy event, checking the staus of my thread conference")
	phone_number = conference_event.getHeader("Caller-Caller-ID-Number", -1)
	print('caller id destroy event is ', str(phone_number))
	
	if not esl.check_conf_alive(self.conference_name):
	    print("[event listener cohort - "+ self.cohort_id+"], yes my conference has ended so now closing myself")
	    self.stop()
	    
#        if "not found" in conference_uuid:
#            print("conference ended ")
#            controller.insert_freewitch_show_end_logs("conference_end", self.show_id, self.conference_name, self.cohort_id)

#            self.stop()
#	else:
#	    print("conference of my thread still live .....")

    def handle_del_conf_member(self,conference_event):

        print("[event listener cohort - "+ self.cohort_id+"]--- Member Delete  Case---")
	phone_number = conference_event.getHeader("Caller-Caller-ID-Number", -1)


	if phone_number:
	    phone_number = phone_number[len(phone_number)-10:]
		
	    if phone_number == self.broadcaster_no:
	        if phone_number in self.conference_connected_listeners:
	            print("[event listener cohort - "+ self.cohort_id+"]HOST CALL DROPPED")
		    self.conference_connected_listeners.remove(phone_number)
		        #print("HOST present in the list, after removing", str(self.conference_connected_listeners))
		    if self.dial_listeners_flag == 1:
			print("size of connected callers list", len(self.conference_connected_listeners))
  	                controller.insert_broadcaster_show_call_logs("conference_host_call_drop", self.show_id, self.conference_name, phone_number, self.cohort_id, "none")
                        print("[event listener cohort - "+ self.cohort_id+"]Redialling the host")
	                    #if esl.check_conf_alive :
	
		        dial_result = esl.add_listener_to_conference(phone_number, self.show_id, config.locale, self.conference_name, self.cohort_id, "unmute","conference_host_redial", self.conf_recording_path, self.show_thread_dict[self.broadcaster_no])
	                if dial_result == "none":
                        	print("redialling failed at the freeswitch side, possible cause, the conference might have destroyed by the time this phone" )
           		else:
				esl.play_audio_conference(self.conference_name, config.host_call_drop)
	

		    else:
			    print("[event listener cohort - "+ self.cohort_id+"] - no listeners has been called yet so not redialling the host")

	    elif phone_number in self.cohort_members:
		#time.sleep(2)
		if esl.check_conf_alive(self.conference_name) :

		    #checking whether listener was earlier in the connected listeners list or not, if yes then now it needs to be removed
                    if phone_number in self.conference_connected_listeners:
                        print("[event listener cohort - "+ self.cohort_id+"]Conference Member of my cohort dropped")
                        self.conference_connected_listeners.remove(phone_number)


	                name = connectSQL.get_use_name(phone_number)

                	#if name != 'none':
	                    # send data to broadcaster to deactivate asha
			#    data = {"objective" : "conf_member_status", "phoneno" : name , "show_id" : self.show_id , "conference_name" : self.conference_name, "task" : "offline"}
			#else:
			data = {"objective" : "conf_member_status", "phoneno" : phone_number , "show_id" : self.show_id , "conference_name" : self.conference_name, "task" : "offline"}

                        json_data = json.dumps(data)
                        broadcaster_publisher.send(json_data , self.broadcaster_no, "2")                   

                        print("[event listener cohort - "+ self.cohort_id+"]Redialling")
			if esl.check_conf_alive(self.conference_name):
                            dial_result = esl.add_listener_to_conference(phone_number, self.show_id, config.locale, self.conference_name, self.cohort_id, "mute","conference_redial", self.conf_recording_path, self.show_thread_dict[self.broadcaster_no])
		            controller.insert_listener_show_call_logs("conference_listener_call_drop", self.show_id, self.conference_name, phone_number, self.cohort_id)
			    if dial_result == "none":
				print('redialling failed at the freeswitch side, possible cause, the conference might have destroyed by the time this phone no was being redialled to add into that conference')
			else:
			    print("[event listener cohort - "+ self.cohort_id+"]on checking again the conference status, found destroyed , so not redialling")



	else:
	        print("[event listener cohort - "+ self.cohort_id+"]conf member delete event--no phone number captured")


	
	#else:
	 #   print("[event listener cohort - "+ self.cohort_id+"]Member deleted after conference has been destroyed, not taking any action")

	 #   if phone_number:
         #       phone_number = phone_number[len(phone_number)-10:]
        #	print("[event listener cohort - "+ self.cohort_id+"]phone number of the dropped person is ", phone_number)
 

    def handle_conference_media_stop(self,conference_event):

        #checking for media stop event only when some media of this conference was playing, checking flag for this
	if self.playback_flag != "none": 

	    #if esl.get_play_status(self.conference_name):
	    if "Nothing is playing" in esl.get_play_status(self.conference_name):

		print('the media of my conference has stopped')
                now = datetime.datetime.now()
                now = now.strftime("%Y-%m-%d %H:%M:%S")

                print("[event listener cohort - "+ self.cohort_id+"]current audio of my conference thread has stopped")
                data = {'objective' : 'media_stopped', 'case':self.playback_flag, 'media_order': self.playback_orderno, 'show_id' : self.show_id,'conference_name': self.conference_name, 'timestamp' : now}

                json_data = json.dumps(data)
                broadcaster_publisher.send(json_data , self.broadcaster_no, "1")

                mongo.insert_play_pause_stats(data)

                self.playback_flag = "none"
		self.playback_orderno = "-1"




 
    def handle(self, conference_event):

        event_calling_function = conference_event.getHeader("Event-Calling-Function", -1)
        event_name = conference_event.getHeader("Event-Name", -1)
#        print("event_calling_function....", event_calling_function)
            
        if event_name == "CUSTOM":
            action = conference_event.getHeader('Event-Subclass')
            
            if action == 'conference::maintenance':
                conf_action = conference_event.getHeader('Action')
		#print("conf action---->", conf_action)

                if conf_action == 'conference-destroy':
                    print("[event listener cohort - "+ self.cohort_id+"]--- Conference Destroy ---")
                    self.handle_conference_end(conference_event)
                
                   
                    
                elif (conf_action == 'unmute-member') or (conf_action == 'mute-member'):
                    #print('--- Member Mute/Unmute ---')
                    self.handle_mute_unmute(conference_event,conf_action)
               
                elif (conf_action == 'start-talking') or (conf_action == 'stop-talking'):
                    #print('---started speaking---')
                    self.handle_speak_events(conference_event, conf_action)
                    
                #elif (conf_action == 'kick-member'):
                elif (conf_action == 'del-member'):
                    
		    self.handle_del_conf_member(conference_event)		

	        elif (conf_action == 'play-file-done' and self.playback_flag != 'none'):
		    #print("flaggggg is ", str(self.playback_flag))
                    print("[event listener cohort - "+ self.cohort_id+"]COntent STOPPED..")
       	            self.handle_conference_media_stop(conference_event)

        if event_name == "CHANNEL_ANSWER":
            #self.counter = self.counter + 1
            print("[event listener cohort - "+ self.cohort_id+"]--- Channel Answer ---")            
            #print('Counter is ' , self.counter)
            self.handle_channel_answer(conference_event)			
        
        

        if event_name == "DTMF":
            #print("DTMF event....")
            self.handle_key_press(conference_event)


        
 
			
    def run(self):
        print("[event listener cohort - "+ self.cohort_id+"]--- Event Thread Started ---")
        #print('parameters received:broadcaster, cohort, conference ', self.broadcaster_no, self.cohort_id, self.conference_name)
        freeswitch_connection = create_freeswitch_connection()
           
        listeners = connectSQL.get_listeners(self.cohort_id)
        for listener in listeners:
            self.cohort_members.append(str(listener[0]))
        
        
        while self._is_running:
            
            e = freeswitch_connection.recvEvent()
#            if esl.check_conf_alive(self.studio_id) == True:
#            if esl.check_conf_alive(self.studio_id) == True:
            self.handle(e)
#            else:
#                self.stop() 
        print("[event listener cohort - "+ self.cohort_id+"]--- Event Thread Closed ---")
