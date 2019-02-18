from flask import Flask
from flask_pymongo import PyMongo
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'sangoshthi_audio'
app.config['MONGO_URI'] = 'mongodb://192.168.2.71:27017/sangoshthi_audio'

mongo = PyMongo(app)



phoneno = '9716517818'



def get_msg_body_by_id(msg_id):
    with app.app_context():
        entries  =   mongo.db.notification_pool
        for q in entries.find():
            for q1 in q['messages_data']:
                if q1['msg_id'] == msg_id:
                    return q1['body']

def check_user_notification_status(msg_id):

    with app.app_context():
        entries  =   mongo.db.user_notification_status

        for q3 in entries.find():
            if q3['phoneno'] == phoneno:
                print("user notification data is "+json.dumps(q3['data']))
                for entry in q3['data']:
                    if entry['msg_id'] == q1['msg_id']:
                        print("present exiting")
                        return "found"
                    else:
                        continue

        return "not found"



def update_notification(msg_id,body, phone):
    #obj = '{"phoneno":"'+phone+ '"}, {"$addToSet": {"data":{"msg_id" : "' + msg_id +'", "body" : "'+body+'", "read_status" : "0"}}}'
    print("prepared new notification is ",obj)
    #parsed_obj = json.loads(obj)
    
    with app.app_context():
       #mongo.db.user_notification_status.update(str(obj))
       mongo.db.user_notification_status.update({"phoneno": phone }, {"$addToSet":{"data":{"msg_id" : msg_id, "body" : body, "read_status" : "0"}}})   

            


def prepare_json_packet_user():
    #json_obj = '{"objective": "notify", "data":{'+'"
    with app.app_context():
        entries  =   mongo.db.user_notification_status
        for q in entries.find():
            if q['phoneno'] == phoneno:
                notification_list = q['data']
    print(notification_list)
 
    




with app.app_context():
    message_id_list = []
    entries  =   mongo.db.notification_user_mapping
    found_flag = 0

    for q in entries.find():
        for q1 in q['mapping']:
            if any(phoneno in s for s in q1['recipient_list']):
                print("recipient found")
                message_id_list.append(q1['msg_id'])
                print("for msg id "+q1['msg_id']+ " going to check whether its data is there or not")
               
                msg_status = check_user_notification_status(q1['msg_id'])
                if msg_status == "not found":
                    #if found_flag == 1:
                    #    json_obj = json_obj + ', {'

                    #json_obj = json_obj + '"msg_id":"'+ q1['msg_id']+'", '
                    #print("updated json "+json_obj)
                    body = get_msg_body_by_id(q1['msg_id'])
                    print("body fetched is "+body)
 
                    #json_obj = json_obj + '"body":"'+body+'", "read_status":"0"}'
                    
                    update_notification(q1['msg_id'],body,phoneno)
                    
                    found_flag = 1

                else:
                    continue

    prepare_json_packet_user()









'''

 entries  =   mongo.db.user_notification_status
                for q3 in entries.find():
                    if q3['phoneno'] == phoneno:
                        print("user notification data is "+json.dumps(q3['data']))
                        for entry in q3['data']:                        
                            if entry['msg_id'] == q1['msg_id']:
                                print("loop over")
                            else:
                                json_obj = json_obj + '"msg_id":"'+ q1['msg_id']+'", '
                                print("updated json "+json_obj)
                                body = get_msg_body_by_id(q1['msg_id'])
                                print("body fetched is "+body)
                                
                                json_obj = json_obj + '"body":"'+body+'", "read_status":"0"}'
'''
