import controller as ctrl
import esl_controller as esl
import test_event_listener
import time



broadcaster_no = "8377843489"
ctrl.call_conference_host(broadcaster_no,"conf2")
print("starting conference thread2......")
thread = test_event_listener.EventListenerThread("conf2")
thread.start()

esl.add_listener_to_conference("8377840906", "91", "conf2", "mute","conference")



