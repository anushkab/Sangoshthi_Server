

#!/usr/bin/env python
import pika
import json
import yaml


# rabbitmq declarations
credentials_b_s = pika.PlainCredentials('sangoshthi', 'sangoshthi')
#parameters_b_s = pika.ConnectionParameters('192.168.2.71',5672,'/',credentials_b_s)
parameters_b_s = pika.ConnectionParameters('103.25.231.30',5673,'/',credentials_b_s)
# broadcaster to server
connection_b_s = pika.BlockingConnection()
channel_b_s = connection_b_s.channel()

channel_b_s.queue_declare(queue='broadcaster_to_server_ivr')

asha_list = ["9711716880"]

json_asha_list = json.dumps(asha_list)

print("asha lis is json dumpos", json.dumps(asha_list))
print("asha list is ", str(asha_list))
print("asha list str(json dumps) is ", str(json_asha_list))

#def main(argv):
print "hello I am pseudo android client"

json_obj1 = '{"objective" : "create_show", ' \
             '"show_name" : "test30", ' \
             '"time_of_airing" : "erfs", '\
             '"video_name": "sample video", ' \
             '"broadcaster" : "9716517818", ' \
             '"show_status":"1", ' \
             '"timestamp":"xyz", ' \
             '"list_of_asha" : ["8901174886"]}' 


install = '{"objective" : "app_install_notify", ' \
                    '"broadcaster" : "9716517818", '\
                    '"timestamp" : "sdsf" }'



notify = '{"objective" : "app_launch_notify", ' \
                    '"broadcaster_phoneno" : "9871335244", '\
                    '"broadcaster_email" : "sdsf" }'



broadcaster_info = '{"objective" : "broadcaster_basic_info", ' \
                    '"broadcaster_name" : "test1", ' \
                    '"broadcaster_phoneno" : "erfs", '\
                    '"broadcaster_email" : "sdsf" }'



get_show = '{"objective" : "get_upcoming_show", ' \
              '"broadcaster" : "9716517818", '\
               '"cohort_id" : "1", ' \
               '"timestamp" : "erfs" }'



play_media = '{"objective" : "play_show_content", ' \
              '"broadcaster" : "9716517818", '\
               '"cohort_id" : "1", ' \
               '"show_id" : "show_1", ' \
               '"conference_name" : "show_1_2017_06_15_14_10_15"}'

stop_media = '{"objective" : "stop_show_content", ' \
              '"broadcaster" : "9716517818", '\
               '"cohort_id" : "1", ' \
               '"show_id" : "show_1", ' \
               '"conference_name" : "show_1_2017_06_15_14_10_15"}'


pause_resume_media = '{"objective" : "pause_play_show_content", ' \
               '"show_id" : "show_1", ' \
               '"broadcaster" : "9716517818", '\
               '"cohort_id" : "1", ' \
               '"conference_name" : "show_1_2017_06_15_14_10_15" }'

start_show = '{"objective" : "start_show", ' \
               '"show_id" : "show_1", ' \
               '"broadcaster" : "9716517818", '\
               '"cohort_id" : "1", ' \
               '"timestamp" : "erfs" }'


flush_callers = '{"objective" : "flush_callers", ' \
               '"show_id" : "show_1", ' \
               '"broadcaster" : "9716517818", '\
               '"cohort_id" : "1", ' \
               '"timestamp" : "erfs" }'
           

dial_listeners = '{"objective" : "dial_listeners", ' \
                '"broadcaster" : "9716517818", ' \
              '"show_id" : "show_1", ' \
             '"timestamp" : "erfs", '\
             '"cohort_id" : "1", '\
             '"conference_name": "show_1_2017_06_17_16_16_50"}'


mute = '{"objective" : "mute", '\
       '"show_id" : "show_1", '\
       '"broadcaster" : "9716517818", '\
       '"timestamp" : "erfs", '\
       '"turn" : "3", '\
       '"listener_phoneno" : "8377843489", '\
       '"conference_name": "show_1_2017_06_15_14_10_15"}'

unmute = '{"objective" : "unmute", ' \
         '"show_id" : "show_1", ' \
         '"timestamp" : "erfs", '\
         '"listener_phoneno" : "8377843489", ' \
         '"turn" : "3", '\
         '"broadcaster" : "9716517818", '\
         '"conference_name": "show_1_2017_06_15_14_10_15"}'

flush_data = '{"objective" : "QA_round_flush", ' \
             '"show_name" : "test1", ' \
             '"timestamp" : "18 Apr 2017 11:48:42 a.m.", '\
             '"broadcaster" : "9716517818"}'

end_show = '{"objective" : "end_show_call", ' \
               '"show_id" : "show_1", ' \
               '"broadcaster" : "9716517818", '\
               '"cohort_id" : "1", ' \
	       '"conference_name" : "show_2_2017_06_17_16_27_38", '\
               '"timestamp" : "erfs" }'

test_ttl = '{"objective" : "ttl test", ' \
             '"show_name" : "test1", ' \
             '"timestamp" : "18 Apr 2017 11:48:42 a.m.", '\
             '"broadcaster" : "9716517818"}'


playback = '{"objective" : "show_playback_metadata", ' \
               '"show_id" : "show_1", ' \
               '"broadcaster" : "9716517818", '\
               '"cohort_id" : "1", ' \
               '"timestamp" : "erfs" }'


update_show = '{"objective" : "update_show_status", ' \
               '"show_id" : "show_1", ' \
	       '"status" : "done", ' \
               '"broadcaster" : "9716517818", '\
               '"cohort_id" : "1", ' \
               '"timestamp" : "erfs" }'







print("json obj prepared is ",str(json_obj1))
count = True
while count == True:
    print "1. create show\n2. start show\n3. dial listeners\n4. mute\n5. unmute\n6. flush\n7. broadcaster info update\n8. notify\n9. get upcoming show\n10. install \n11. play media\n12. stop media\n13. pause_resume\n14. flush_callers\n15. ttl testing \n16. playback\n17. end show\n18. update show status\n19. exit menu"
    vals = raw_input("Enter command to test out: ")

    if vals == '1':
        print("create start case")
        json_obj = json.loads(json_obj1)
        print("json obj prepared (str) is  ",str(json_obj))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj))
#       elif vals == 'stop record':
#       json_obj = json.loads(json_record_stop)

	print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj))
#        channel_b_s.basic_publish("",'trainer_to_server',json_obj)


    if vals == '2':
        print("start show case")
        json_obj2 = json.loads(start_show)
        print("json obj prepared (str) is  ",str(json_obj2))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj2))
#       elif vals == 'stop record':
#       json_obj = json.loads(json_record_stop)

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj2))
#        channel_b_s.basic_publish("",'trainer_to_server',json_obj)


    if vals == '3':
        print("dial listeners case")
        json_obj6 = json.loads(dial_listeners)
#        print("json obj prepared (str) is  ",str(json_obj2))
#        print("json obj prepared (json dumps) is  ",json.dumps(json_obj2))
#       elif vals == 'stop record':
#       json_obj = json.loads(json_record_stop)

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj6))
#        channel_b_s.basic_publish("",'trainer_to_server',json_obj)



    if vals == '4':
        print("mute case")
        json_obj3 = json.loads(mute)
        #print("json obj prepared (str) is  ",str(json_obj))
        #print("json obj prepared (json dumps) is  ",json.dumps(json_obj))
#       elif vals == 'stop record':
#       json_obj = json.loads(json_record_stop)

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj3))
#        channel_b_s.basic_publish("",'trainer_to_server',json_obj)



    if vals == '5':
        print("unmute case")
        json_obj4 = json.loads(unmute)
        #print("json obj prepared (str) is  ",str(json_obj))
        #print("json obj prepared (json dumps) is  ",json.dumps(json_obj))
#       elif vals == 'stop record':
#       json_obj = json.loads(json_record_stop)

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj4))
#        channel_b_s.basic_publish("",'trainer_to_server',json_obj)


    if vals == '6':
        print(" flush data case")
        json_obj5 = json.loads(flush_data)
#        print("json obj prepared (str) is  ",str(json_obj))
 #       print("json obj prepared (json dumps) is  ",json.dumps(json_obj))
#       elif vals == 'stop record':
#       json_obj = json.loads(json_record_stop)

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_IVR',body=json.dumps(json_obj5))
#        channel_b_s.basic_publish("",'trainer_to_server',json_obj)


    if vals == '7':
        print(" update broadcaster info")
        json_obj6 = json.loads(broadcaster_info)
        print("json obj prepared (str) is  ",str(json_obj6))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj6))

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_IVR',body=json.dumps(json_obj6))



    if vals == '8':
        print(" notify")
        json_obj7 = json.loads(notify)
        print("json obj prepared (str) is  ",str(json_obj7))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj7))

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj7))


    if vals == '9':
        print(" get upcoming show")
        json_obj8 = json.loads(get_show)
        print("json obj prepared (str) is  ",str(json_obj8))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj8))

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj8))
  


    if vals == '10':
        print(" get upcoming show")
        json_obj8 = json.loads(install)
        print("json obj prepared (str) is  ",str(json_obj8))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj8))

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj8))



    if vals == '11':
#        print(" get upcoming show")
        json_obj11 = json.loads(play_media)
        print("json obj prepared (str) is  ",str(json_obj11))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj11))

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj11))



    if vals == '12':
        print(" get upcoming show")
        json_obj12 = json.loads(stop_media)
        print("json obj prepared (str) is  ",str(json_obj12))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj12))

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj12))


    if vals == '13':
        print("pause resume")
        json_obj13 = json.loads(pause_resume_media)
        print("json obj prepared (str) is  ",str(json_obj13))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj13))

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj13))



    if vals == '14':
        print("pause resume")
        json_obj14 = json.loads(flush_callers)
        print("json obj prepared (str) is  ",str(json_obj14))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj14))

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj14))


    if vals == '15':
        print("per message ttl testing")
        json_obj15 = json.loads(test_ttl)

#        properties = pika.BasicProperties(expiration = '30000')

#        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr', body=json.dumps(json_obj15), properties = properties)
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr', body=json.dumps(json_obj15))



    if vals == '16':
        print("playback ")
        json_obj16 = json.loads(playback)

#        properties = pika.BasicProperties(expiration = '30000')

#        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr', body=json.dumps(json_obj15), properties = properties)
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr', body=json.dumps(json_obj16))


    if vals == '17':
        print("end show ")
        json_obj17 = json.loads(end_show)
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr', body=json.dumps(json_obj17))


    if vals == '18':
        print("update_show_status ")
        json_obj18 = json.loads(update_show)
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr', body=json.dumps(json_obj18))

    if vals == '19':
        count = False
        connection_b_s.close()
        

#if __name__ == '__main__':
#    main()

