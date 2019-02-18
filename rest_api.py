from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from datetime import datetime
from datetime import timedelta
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'SangoshthiDb'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/SangoshthiDb'

mongo = PyMongo(app)

def get_current_time():
    nowDate= datetime.now() - timedelta(minutes = 90)
    DateNow = nowDate.strftime("%Y-%m-%d %H:%M:%S")
    DatePresent = datetime.strptime(DateNow, "%Y-%m-%d %H:%M:%S")
    return DatePresent

@app.route('/shows', methods=['GET'])
def get_all_shows():
    entries = mongo.db.show_stats

    output = []
    DatePresent = get_current_time()

    for q in entries.find():
        if(q["objective"] == "create_show"):
            inDate = q['time_of_airing']
            DateIn = datetime.strptime(inDate, "%d/%m/%Y %H:%M:%S")

            if(DateIn > DatePresent):
                output.append({'ShowName' : q['show_name'] ,
                               'TimeOfAiring' : q['time_of_airing'] ,
                               'AshaList' : q['list_of_asha'] ,
                               'VideoName' : q['video_name'] ,
                               'Broadcaster' : q['broadcaster']})
            
    return jsonify({'result' : output})

@app.route('/shows/ashas', methods=['GET'])
def get_all_ashas():
    entries = mongo.db.show_stats

    output = []
    DatePresent = get_current_time()
    
    for q in entries.find():
        if(q["objective"] == "create_show"):
            inDate = q['time_of_airing']
            DateIn = datetime.strptime(inDate, "%d/%m/%Y %H:%M:%S")

            if(DateIn > DatePresent):
                listAsha = q['list_of_asha']

                for asha in listAsha:
                    output.append({'AshaName' : asha ,
                                   'ShowName' : q['show_name'] ,
                                   'TimeOfAiring' : q['time_of_airing'],
                                   'VideoName' : q['video_name'] ,
                                   'Broadcaster' : q['broadcaster']})
            
    return jsonify({'result' : output})

@app.route('/shows/ashas/<phone_no>', methods=['GET'])
def get_matching_ashas(phone_no):
    entries = mongo.db.show_stats

    output = []
    DatePresent = get_current_time()

    for q in entries.find():
        if(q["objective"] == "create_show"):
            inDate = q['time_of_airing']
            DateIn = datetime.strptime(inDate, "%d/%m/%Y %H:%M:%S")
            listAsha = []
            
            if(DateIn > DatePresent):
                listAsha = q['list_of_asha']

                if(phone_no in listAsha):
                    output.append({'ShowName' : q['show_name'] ,
                                   'TimeOfAiring' : q['time_of_airing'] ,
                                   'VideoName' : q['video_name'] ,
                                   'Broadcaster' : q['broadcaster']})

    return jsonify({'result' : output})

@app.route('/shows/broadcasters', methods=['GET'])
def get_all_broadcasters():
    entries = mongo.db.show_stats

    output = []
    DatePresent = get_current_time()
    
    for q in entries.find():
        if(q["objective"] == "create_show"):
            inDate = q['time_of_airing']
            DateIn = datetime.strptime(inDate, "%d/%m/%Y %H:%M:%S")

            if(DateIn > DatePresent):
                output.append({'Broadcaster' : q['broadcaster'] ,
                                'ShowName' : q['show_name'] ,
                                'TimeOfAiring' : q['time_of_airing'] ,
                                'AshaList' : q['list_of_asha'] ,
                                'VideoName' : q['video_name']})

            
    return jsonify({'result' : output})

@app.route('/shows/broadcasters/<phone_no>', methods=['GET'])
def get_matching_broadcasters(phone_no):
    entries = mongo.db.show_stats

    output = []
    DatePresent = get_current_time()
    
    for q in entries.find():
        if(q["objective"] == "create_show"):
            inDate = q['time_of_airing']
            DateIn = datetime.strptime(inDate, "%d/%m/%Y %H:%M:%S")
            listAsha = []
            
            if(DateIn > DatePresent):
                if(q['broadcaster'] == phone_no):
                    output.append({'ShowName' : q['show_name'] ,
                                   'TimeOfAiring' : q['time_of_airing'] ,
                                   'AshaList' : q['list_of_asha'] ,
                                   'VideoName' : q['video_name']})

    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(host='192.168.2.71' , port=8000 , debug=True)
