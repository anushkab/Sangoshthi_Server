from flask import Flask
from flask_pymongo import PyMongo
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'SangoshthiDb'
app.config['MONGO_URI'] = 'mongodb://192.168.2.71:27017/SangoshthiDb'

mongo = PyMongo(app)

# NETWORK COMMANDS

# create a new show
def insert_show_stats(data):

    with app.app_context():
        entries = mongo.db.show_stats
        status = entries.insert(data)
        print(data)
        return status

# play/pause commands
def insert_play_pause_stats(data):

     with app.app_context():
        entries = mongo.db.play_pause_stats
        status = entries.insert(data)
        print(data)
        return status

# flush query
def insert_flush_query_stats(data):

     with app.app_context():
        entries = mongo.db.flush_query_stats
        status = entries.insert(data)
        print(data)
        return status
    
# asha has raised a query
def insert_asha_query_stats(data):

    with app.app_context():
        entries = mongo.db.asha_query_stats
        status = entries.insert(data)
        print(data)
        return status
        
# asha liked the video
def insert_asha_like_stats(data):

    with app.app_context():
        entries = mongo.db.asha_like_stats
        status = entries.insert(data)
        print(data)
        return status

# get show status if finished or not, if finished then return 0 else 1
def get_show_status(show_name):
    
    with app.app_context():
        entries = mongo.db.show_stats
        
        for q in entries.find():
            if(q['show_name'] == show_name):
                return q['show_status']

        return 0

# FREESWITCH COMMANDS

# schedule the broadcast of trailer
def insert_spread_word_stats(data):

    with app.app_context():
        entries = mongo.db.spread_word_stats
        entries.insert(data)
        print(data)

# add delete listener stats
def insert_del_listener_stats(data):

    with app.app_context():
        entries = mongo.db.del_listener_stats
        status = entries.insert(data)
        print(data)
        return status
        
# delete listener from show_stats table
def del_listener(show_name , phone):
    
    with app.app_context():
        entries = mongo.db.show_stats        
        status = entries.update({"show_name":show_name},{"$pull" : {"list_of_asha" : phone}})
        return status

# add delete all listeners stats
def insert_del_all_listener_stats(data):

    with app.app_context():
        entries = mongo.db.del_all_listener_stats
        status = entries.insert(data)
        print(data)
        return status

# delete all listeners from show_stats table     
def del_all_listener(show_name):
    
    with app.app_context():
        entries = mongo.db.show_stats        
        status = entries.update({"show_name":show_name},{"$set" : {"list_of_asha" : []}})
        return status

# add play trailer stats
def insert_play_trailer_stats(data):

     with app.app_context():
        entries = mongo.db.play_trailer_stats
        status = entries.insert(data)
        print(data)
        return status

# add delete trailer stats
def insert_delete_trailer_stats(data):

    with app.app_context():
        entries = mongo.db.delete_trailer_stats
        status = entries.insert(data)
        print(data)
        return status

# add call broadcaster stats
def insert_call_broadcaster_stats(data):
    with app.app_context():
        entries = mongo.db.call_broadcaster_stats
        status = entries.insert(data)
        print(data)
        return status
    
# get broadcaster for a specific show
def get_broadcaster_from_db(show_name):

    with app.app_context():
        entries = mongo.db.show_stats
        
        for q in entries.find():
            if(q['show_name'] == show_name):
                return q['broadcaster']

        return 0

# add call listener stats
def insert_call_listener_stats(data):
    with app.app_context():
        entries = mongo.db.call_listener_stats
        status = entries.insert(data)
        print(data)
        return status
    
# get ashas for a specific show
def get_ashas_from_db(show_name):

    with app.app_context():
        entries = mongo.db.show_stats
        
        for q in entries.find():
            if(q['show_name'] == show_name):
                return q['list_of_asha']

        return 0

# add mute/unmute stats
def insert_mute_unmute_stats(data):

    with app.app_context():
        entries = mongo.db.mute_unmute_stats
        status = entries.insert(data)
        print(data)
        return status

# update show stats flag when show ends
def update_show_stats(show_name):

    with app.app_context():
        entries = mongo.db.show_stats        
        status = entries.update({"show_name":show_name},{"$set" : {"show_status" : '0'}})
        return status

# get show status
def get_show_status(show_name)

    with app.app_context():
        entries = mongo.db.show_stats        

        for q in entries.find():
            if(q['show_name'] == show_name):
                return q['show_status']
            
        return 0
