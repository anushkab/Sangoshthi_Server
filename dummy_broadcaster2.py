
#!/usr/bin/env python
import pika
import json
import yaml


# rabbitmq declarations
credentials_b_s = pika.PlainCredentials('sangoshthi', 'sangoshthi')
parameters_b_s = pika.ConnectionParameters('192.168.2.71',5672,'/',credentials_b_s)

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






notify = '{"objective" : "app_launch_notify", ' \
                    '"broadcaster_phoneno" : "9871335244", '\
                    '"broadcaster_email" : "sdsf" }'



broadcaster_info = '{"objective" : "broadcaster_basic_info", ' \
                    '"broadcaster_name" : "test1", ' \
                    '"broadcaster_phoneno" : "erfs", '\
                    '"broadcaster_email" : "sdsf" }'



start_show = '{"objective" : "start_show", ' \
               '"show_id" : "show_2", ' \
               '"broadcaster" : "8377846695", '\
               '"cohort_id" : "3", ' \
               '"timestamp" : "erfs" }'
            

flush_callers = '{"objective" : "flush_callers", ' \
               '"show_id" : "show_2", ' \
               '"broadcaster" : "8377846695", '\
               '"cohort_id" : "3", ' \
               '"timestamp" : "erfs" }'




dial_listeners = '{"objective" : "dial_listeners", ' \
                '"broadcaster" : "8377840906", ' \
              '"show_id" : "show_2", ' \
             '"timestamp" : "erfs", '\
             '"cohort_id" : "3", '\
             '"conference_name": "show_2_2017_06_07_16_08_25"}'


mute = '{"objective" : "mute", '\
       '"show_id" : "show_2", '\
       '"broadcaster" : "8377840906", '\
       '"timestamp" : "erfs", '\
       '"turn" : "1", '\
       '"listener_phoneno" : "8377846695", '\
       '"conference_name": "show_2_2017_06_07_16_08_25"}'

unmute = '{"objective" : "unmute", ' \
         '"show_id" : "show_2", ' \
         '"timestamp" : "erfs", '\
         '"turn" : "1", '\
         '"listener_phoneno" : "8377846695", ' \
         '"broadcaster" : "8377840906", '\
         '"conference_name": "show_2_2017_06_07_16_08_25"}'

flush_data = '{"objective" : "QA_round_flush", ' \
             '"show_name" : "test1", ' \
             '"timestamp" : "18 Apr 2017 11:48:42 a.m.", '\
             '"broadcaster" : "9716517818"}'


print("json obj prepared is ",str(json_obj1))
count = True
while count == True:
    print "1. create show\n2. start show\n3. dial listeners\n4. mute\n5. unmute\n6. flush\n7. broadcaster info update\n8. notify\n9 flush callers\n11.exit menu"
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
        print(" flush callers")
        json_obj8 = json.loads(flush_callers)
        print("json obj prepared (str) is  ",str(json_obj8))
        print("json obj prepared (json dumps) is  ",json.dumps(json_obj8))

        print "sending to rabbitmq queue"
        channel_b_s.basic_publish(exchange='',routing_key='broadcaster_to_server_ivr',body=json.dumps(json_obj8))


    if vals == '11':
        count = False
        connection_b_s.close()
        

#if __name__ == '__main__':
#    main()

