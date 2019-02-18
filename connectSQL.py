try:
    import fs_config as config
    import MySQLdb
    import datetime
    import json
    import pytz
except:
    print "Error importing modules.."

try:
    standardQuery = "SELECT VERSION()"
#    db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
    # prepare a cursor object using cursor() method
    
#    cursor = db.cursor()
except:
    print "Error connecting SQL"



def close_db_connection():
    print("closing db connection")
    db.close()


def get_content_for_show(show_id):
    query1 = "select content_id from Sangoshti_Django.WebPortal_show where showID = '"+show_id+"'" 
    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()	
        cursor.execute(query1)
        content_id = cursor.fetchone()
        print("content_id fetched is",str(content_id[0]))
        query2 = "select audiofile_id from Sangoshti_Django.WebPortal_content_files where content_id  = '"+str(content_id[0])+"'"
        cursor.execute(query2)
        audiofile_id = cursor.fetchone()
        query3 = "select file from Sangoshti_Django.WebPortal_audiofile where id = '" + str(audiofile_id[0]) + "'"
        cursor.execute(query3)
        audiofile_path = cursor.fetchone()
	cursor.close()
	db.close()
        return str(audiofile_path[0])
    except:
        print "exception in receiving content files path"
        return "none"





def update_show_status(show_id, status):
    query1 = 'update WebPortal_show set status = \''+ str(status)+ '\' where showID = \''+show_id +'\''
    print("query is", query1)
    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()
        return_val = cursor.execute(query1)
	print(str(return_val))
	db.commit()
  	cursor.close()
	db.close()
        return "OK"
    except:
        print "exception in receiving the cohortID"
        return "none"





def get_cohortID_from_phoneno(phone):

    query1 = 'select WebPortal_cohort_listeners.cohort_id from WebPortal_cohort_listeners INNER JOIN WebPortal_asha ON ' \
             'WebPortal_cohort_listeners.asha_id = WebPortal_asha.id where WebPortal_asha.phoneNumber =\''+phone+'\''

    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()
        cursor.execute(query1)
        cohort_id = cursor.fetchone()
	cursor.close()
	db.close()
	if cohort_id:
            return str(cohort_id[0])
	else:
	    return "none"
    except:
        print "exception in receiving the cohortID"
        return "none"

 
    
def get_listeners(cohort_id):
    query1 = 'select WebPortal_asha.phoneNumber from WebPortal_asha INNER JOIN WebPortal_cohort_listeners ON' \
             ' WebPortal_cohort_listeners.asha_id = WebPortal_asha.id where WebPortal_cohort_listeners.cohort_id = \''+cohort_id+'\''
    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()
        cursor.execute(query1)
        phone_numbers = cursor.fetchall()
	cursor.close()
	db.close()
        return phone_numbers
    except:
        print "exception in listeners numbers"
        return "none"


def get_cohort_members_name_phone_mapping(cohort_id):

    query1 = 'select WebPortal_asha.phoneNumber, WebPortal_asha.name  from WebPortal_asha INNER JOIN WebPortal_cohort_listeners ON' \
             ' WebPortal_cohort_listeners.asha_id = WebPortal_asha.id where WebPortal_cohort_listeners.cohort_id = \''+cohort_id+'\''
    try:
        db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
        cursor = db.cursor()
        cursor.execute(query1)
        mapping = cursor.fetchall()
        cursor.close()
        db.close()
        return mapping
    except:
        print "exception in listeners numbers"
        return "none"



def get_use_name(phone_number):
    query1 = 'select WebPortal_asha.name from WebPortal_asha where phoneNumber = \'' + phone_number + '\''
    try:
        db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
        cursor = db.cursor()
        cursor.execute(query1)
        name = cursor.fetchone()
        cursor.close()
        db.close()
        return name[0]
    except:
        print "exception in listeners numbers"
        return "none"


def convert_utc_ist(time_string):
    print("time string received", time_string)
    utc_time = datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')
    print(str(utc_time))
    local_tz = pytz.timezone('Asia/Kolkata')
    utc_time = pytz.utc.localize(utc_time) #converting utc time object to utc timezone
    local_time = utc_time.astimezone(local_tz) # converting utc to local Asia/ist timezone
    print("the local time is", str(local_time))
    parsed_time_string  = str(local_time).split('+')
    print(parsed_time_string[0])
    return parsed_time_string[0]
    
    


def get_upcoming_showID(cohort_id):
    query1 = 'select showID from WebPortal_show where cohort_id = \'' + cohort_id + '\' and status = \'0\''
    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()
        cursor.execute(query1)
        show_id = cursor.fetchone()
	cursor.close()
	db.close()
	if show_id:
            return show_id[0]
	else:
	    return "none"
    except:
        print "exception in fetching the show_id"
        return "none"
 

def get_upcoming_show_time(cohort_id):
    query1 = 'select timeOfAiring from WebPortal_show where cohort_id = \'' + cohort_id + '\' and status = \'0\''
    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()
        cursor.execute(query1)
        timeofairing = cursor.fetchone()
	cursor.close()
	db.close()
	if timeofairing:

	    timeofairing = convert_utc_ist(str(timeofairing[0]))
	    return timeofairing
	else:
	    return "none"
    except:
        print "exception in fetching the time of airing"
        return "none"

def get_upcoming_show_localized_topic_name(cohort_id):
    query1 = 'select localized from WebPortal_show INNER JOIN WebPortal_content ON WebPortal_show.content_id = WebPortal_content.id '\
             'where WebPortal_show.cohort_id = \'' + cohort_id + '\' and WebPortal_show.status = \'0\''

    print(query1)
    try:
	#db.set_character_set('utf8_unicode_ci')
        db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute(query1)
        local_name =  cursor.fetchone()
        cursor.close()
        db.close()
        if local_name[0]:
	    #print('localized name fetchhed is '+local_name[0])
	    print('local name is '+local_name[0])
            return local_name[0]
        else:
            return "none"
    except:
        print "exception in fetching the local name of the content"
	return "none"


def get_upcoming_show_topic(cohort_id):
    query1 = 'select name from WebPortal_show INNER JOIN WebPortal_content ON WebPortal_show.content_id = WebPortal_content.id '\
             'where WebPortal_show.cohort_id = \'' + cohort_id + '\' and WebPortal_show.status = \'0\''
    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()
        cursor.execute(query1)
        show_topic =  cursor.fetchone()
	cursor.close()
	db.close()	
	if show_topic:	
            return show_topic[0]
	else:
	    return "none"
    except:
        print "exception in fetching the show topic"
        return "none"


def get_contentID_for_show(show_id):

    query1 = 'select content_id from WebPortal_show where showID = \'' + show_id + '\''

    try:
        db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
        cursor = db.cursor()
        cursor.execute(query1)
        content_id =  cursor.fetchone()
        cursor.close()
        db.close()
        if content_id:
            return content_id[0]
        else:
            return "none"
    except:
        print "exception in fetching the show topic"
        return "none"




def get_cohortID_from_broadcasterno(broadcaster_no):

    query1 = 'select WebPortal_cohort.id from WebPortal_cohort INNER JOIN WebPortal_asha ON ' \
             'WebPortal_cohort.broadcaster_id = WebPortal_asha.id where WebPortal_asha.phoneNumber =\''+broadcaster_no+'\''

    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()
        cursor.execute(query1)
        cohort_id = cursor.fetchone()
	cursor.close()
	db.close()
	if cohort_id:
            return str(cohort_id[0])
	else:
	    return "none"
    except:
        print "exception in receiving the cohortID"
        return "none"



def get_feedback_status(show_id):

    query1 = 'select WebPortal_showfeedback.feedbackFile from WebPortal_showfeedback INNER JOIN WebPortal_show ON WebPortal_showfeedback.show_id = ' \
             'WebPortal_show.id where WebPortal_show.showID  =  \'' + show_id + '\''

    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()
        cursor.execute(query1)
	feedback_file = cursor.fetchone()
	cursor.close()
	db.close()
	if feedback_file:
            return str(feedback_file[0])
	else:
	    return "none"
    except:
        print "exception in receiving the cohortID"
        return "none"


def get_content_status(show_id):

    query1 =  'select content_id from WebPortal_show where showID = \''+show_id+'\''
    try:
	db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
	cursor = db.cursor()
        cursor.execute(query1)
        content_id = cursor.fetchone()
	cursor.close()
	db.close()
	if content_id:
            return str(content_id[0])
	else:
	    return "none"
	
    except:
        print "exception in receiving the cohortID"
        return "none"



def get_broadcaster_from_cohortID(cohort_id):
    query1 =  'select WebPortal_asha.phoneNumber from WebPortal_asha INNER JOIN WebPortal_cohort ON WebPortal_cohort.broadcaster_id = WebPortal_asha.id' \
	      ' where WebPortal_cohort.id = \''+cohort_id+'\''

    try:
        db = MySQLdb.connect(config.sql_host,config.sql_user,config.sql_pass,config.portal_db)
        cursor = db.cursor()
        cursor.execute(query1)
        broadcaster = cursor.fetchone()
        cursor.close()
        db.close()
        if  broadcaster:
            return str(broadcaster[0])
        else:
            return "none"

    except:
        print "exception in receiving the cohortID"
        return "none"





#close_db_connection()
