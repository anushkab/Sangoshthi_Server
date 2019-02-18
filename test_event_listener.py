import traceback, sys
import datetime

try:
    import ESL
    import fs_config as configuration
    import esl_controller as esl
    import threading
    import json
    from threading import Thread
    #from datetime import datetime

except:
    print("Error importing custom modules")
    print(traceback.print_exc())



def create_freeswitch_connection():
    freeswitch_connection = ESL.ESLconnection(configuration.server, configuration.port, configuration.password)
    if not freeswitch_connection.connected():
        print('Not Connected')
        sys.exit(2)
    freeswitch_connection.events('plain', 'all')
   # freeswitch_connection.events('myevents', uuid)
    return freeswitch_connection



class EventListenerThread(Thread):

    def __init__(self, studio_id):
        self.studio_id = studio_id
#        self.uuid = uuid
        self._is_running = True
#        self.callers_count = 0
        Thread.__init__(self)

    def stop(self):
        self._is_running = False


    def handle_channel_answer(self,conference_event):
        phone_number = conference_event.getHeader("Caller-Caller-ID-Number", -1);
        print("channel answered by ", phone_number)
    
    def handle_mute_unmute(self, conference_event, state):

        phone_number = conference_event.getHeader("Caller-Caller-ID-Number", -1);

	print("muted phone number is", phone_number)


    def handle(self, conference_event):
        global flush_callers
        event_calling_function = conference_event.getHeader("Event-Calling-Function", -1)
        event_name = conference_event.getHeader("Event-Name", -1)
        print("event_calling_function", event_calling_function)
        print("event name", event_name)
	if event_name == "CUSTOM":
            action = conference_event.getHeader('Event-Subclass')

            if action == 'conference::maintenance':
                conf_action = conference_event.getHeader('Action')
                conf_uuid = conference_event.getHeader('Core-UUID')
                event_from =  conference_event.getHeader('from')
                print('conf_action ', conf_action, ' event_from ', event_from)
    
    def run(self):
        print('--- Test Event Thread Started ---')
        freeswitch_connection = create_freeswitch_connection()
        #recording conference


        while self._is_running:

            e = freeswitch_connection.recvEvent()
#            if esl.check_conf_alive(self.studio_id) == True:
#            if esl.check_conf_alive(self.studio_id) == True:
            self.handle(e)
#            else:
#                self.stop()
        print('--- Event Thread Closed ---')

