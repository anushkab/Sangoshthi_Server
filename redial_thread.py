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
import eslcontroller as esl
import time
import mongo_file as mongo

def create_freeswitch_connection():
    freeswitch_connection = ESL.ESLconnection(configuration.server, configuration.port, configuration.password)
    if not freeswitch_connection.connected():
            print 'Not Connected'
            sys.exit(2)

    freeswitch_connection.events('plain', 'all')
    return freeswitch_connection

class Redial(Thread):
    
    def __init__(self,studio,phone_number,command,redial_case):
            self.phone_number = phone_number
            self.gateway = configuration.gateway
            self._is_running = True
            self.studio = studio
            self.redial_count = 1   
            self.command = command
            self.con = ""
            self.redial_case = redial_case
            Thread.__init__(self)
            
    
    def update_db(self):
        print('in update db')


    def update_hangupcause(self,cause):
        print('updating listener record hangup causes')
        
    
    def run(self):
        self.con = create_freeswitch_connection()
        print.info('--- Redial Thread Started ---')
         
        while self._is_running:
            
            conference_event = (self.con).recvEvent()
            event_name = conference_event.getHeader("Event-Name", -1)
            
            if event_name == "CHANNEL_HANGUP" :
                
                if self.redial_count != 3:
                    if get_show_status:
                        cause = conference_event.getHeader("Hangup-Cause",-1)
                        hangup_number = conference_event.getHeader("Caller-Caller-ID-Number",-1)
                        
                        print('Hangup Reason: ' + cause)
                        if str(hangup_number) == str(self.phone_number):
                           
                            print('Hangup Case Redialling Again')
                            callresult = (self.con).api(self.command)
                            print("Redial Thread, Command Output is " + str(callresult.getBody()))
                            
                            self.update_hangupcause(cause)
                            self.redial_count += 1
                            print "count now is "+str(self.redial_count)
                    else:
                        print('Show Ended, Stopping Thread')
                        self._is_running = False
                            
                else:
                    print('redial count timeout, stopping redial thread')
                    self.update_db()#"no_response"
                    self._is_running = False
                   
            elif event_name == "CHANNEL_ANSWER":
                number = conference_event.getHeader("Caller-Caller-ID-Number",-1)
                if str(number) == str(self.phone_number):
                                            
                    print('channel is answered by %s stopping redial thread',self.phone_number)
                    self.update_db()#"answer"
                    print "exiting"
                    self._is_running = False
                        
        print.info('Stopped')
                        
                
                

                    
