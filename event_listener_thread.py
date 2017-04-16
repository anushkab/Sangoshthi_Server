import traceback, sys

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("[event_listener_thread]")

try:
    import ESL
    import fs_config as configuration
    import esl_controller as esl
    import threading
    import json
    from threading import Thread
    from datetime import datetime
    
except:
    logger.error("Error importing custom modules")
    logger.error(traceback.print_exc())

def create_freeswitch_connection():
    freeswitch_connection = ESL.ESLconnection(configuration.server, configuration.port, configuration.password)
    if not freeswitch_connection.connected():
        logger.error('Not Connected')
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
                    logger.info('--- Conference Destroy ---')
                    self.stop()
                    
                elif (conf_action == 'unmute-member') or (conf_action == 'mute-member'):
                    logger.info('--- Member Mute/Unmute ---')
                    
                elif (conf_action == 'del-member'):
                    self.counter = self.counter - 1
                    logger.info('Counter is ' , self.counter)
                    logger.info('--- Member Delete ---')
                    
        
        if event_name == "CHANNEL_ANSWER":
            self.counter = self.counter + 1
            logger.info('Counter is ' , self.counter)
            logger.info('--- Channel Answer ---')
			
			
    def run(self):
        logger.info('--- Event Thread Started ---')
        freeswitch_connection = create_freeswitch_connection()
        
        while self._is_running:
            
            e = freeswitch_connection.recvEvent()

            if esl.check_conf_alive(self.studio_id) == True:
                self.handle(e)
            else:
                self.stop()
        logger.info('--- Event Thread Closed ---')
