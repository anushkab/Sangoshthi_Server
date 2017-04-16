import traceback, sys

try:
    import ESL
    import fs_config as configuration
    import esl_controller as esl
    import threading
    import json
    from threading import Thread
    from datetime import datetime
    
except:
    print("Error importing custom modules")
    print(traceback.print_exc())

def create_freeswitch_connection():
    freeswitch_connection = ESL.ESLconnection(configuration.server, configuration.port, configuration.password)
    if not freeswitch_connection.connected():
        print('Not Connected')
        sys.exit(2)
    freeswitch_connection.events('plain', 'all')
    return freeswitch_connection
	
		
class EventListenerThread(Thread):

    def __init__(self, studio_id):
        self.studio_id = studio_id
        self._is_running = True
        self.counter = 0
        Thread.__init__(self)

    def stop(self):
        self._is_running = False

    def handle(self, conference_event):

        event_calling_function = conference_event.getHeader("Event-Calling-Function", -1)
        event_name = conference_event.getHeader("Event-Name", -1)
        
            
        if event_name == "CUSTOM":
            action = conference_event.getHeader('Event-Subclass')
            
            if action == 'conference::maintenance':
                conf_action = conference_event.getHeader('Action')
                
                if conf_action == 'conference-destroy':
                    print('--- Conference Destroy ---')
                    self.stop()
                    
                elif (conf_action == 'unmute-member') or (conf_action == 'mute-member'):
                    print('--- Member Mute/Unmute ---')
                    
                elif (conf_action == 'del-member'):
                    self.counter = self.counter - 1
                    print('Counter is ' , self.counter)
                    print('--- Member Delete ---')
                    
        
        if event_name == "CHANNEL_ANSWER":
            self.counter = self.counter + 1
            print('Counter is ' , self.counter)
            print('--- Channel Answer ---')
			
			
    def run(self):
        print('--- Event Thread Started ---')
        freeswitch_connection = create_freeswitch_connection()
        
        while self._is_running:
            
            e = freeswitch_connection.recvEvent()

            if esl.check_conf_alive(self.studio_id) == True:
                self.handle(e)
            else:
                self.stop()
        print('--- Event Thread Closed ---')
