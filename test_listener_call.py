import controller as ctrl
import esl_controller as esl
import test_event_listener
import time

broadcaster_no = "9716517818"
ctrl.call_conference_host(broadcaster_no,"conf1")
print("starting conference thread")
time.sleep(15)

#uuid = esl.get_conference_uuid("conf1")

thread = test_event_listener.EventListenerThread("conf1")
thread.start()

esl.add_listener_to_conference("8377846695", "new", "91", "conf1", "mute","conference")


