
import os
import django
import sys
import fs_config
import zipfile
from django.core.files import File
sys.path.append('/home/sangoshthi/tushar/Django/Sangoshti')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sangoshti.settings')
django.setup()
from  WebPortal.models import ShowRecording
from  WebPortal.models import Show
from  WebPortal.models import ShowFeedback
from pydub import AudioSegment

#This file is intended to make changes into the Sangoshthi WebPortal from the Sangoshthi server side or get some information from teh portal


"""
from  WebPortal.models import Show
#Show.objects.filter(showID='show_1').update(recording='../recordings/show_1/show_1_combined_recording.wav')


#show = get_show() // assuming you have retrieved a show
show = Show.objects.filter(showID='show_1')[0]
with open('../recordings/show_1/show_1_combined_recording.wav', 'rb') as recording:
   show.recording.save('show_1_combined_recording.wav', File(recording), save=True)
"""




#this function links show recordings to the portal to make them visible there

def update_show_recordings_in_portal(show_id):
        recording_dir = fs_config.recording_dir + show_id
        show = Show.objects.filter(showID = show_id)[0]

        for dir in os.listdir(str(recording_dir)):
                #print("dir", str(dir))
                for recording_file in os.listdir(str(recording_dir)+"/"+dir):
                        #print("level1",recording_file)
                        if ".wav" in recording_file:
                                #print(recording_file)
				newRecording = ShowRecording(show=show,recordingFile=None)
				recordingfile_to_be_uploaded = str(recording_dir + "/"+dir + "/"+recording_file)
				#print("recording files is ",recordingfile_to_be_uploaded)
				with open(recordingfile_to_be_uploaded, 'rb') as recording:
			        	newRecording.recordingFile.save(recording_file, File(recording), save=True)

	return True


#this function give feedback files for show uploaded by the experts			 	
def get_show_feedback_file(show_id):
	#showID = 6
	try:
		show = Show.objects.filter(showID = show_id)[0]
		preFeedback = ShowFeedback.objects.filter(show=show.preFeedback.id).order_by('created_at')
		preFeedback = preFeedback[len(preFeedback)-1]
		print(str(preFeedback))
		file = preFeedback.feedbackFile
		print(file)
		return str(file)
	except:
		return "none"


def get_show_QA1_filepath(show_id):

        try:
                show = Show.objects.filter(showID = show_id)[0]
		QA1_object = show.QA1
		print('retrieved show content path are '+str(QA1_object.file))
                return str(QA1_object.file)
        except:
		print('exception in retrieving show path')
                return "none"
		

def get_show_QA1_localname(show_id):

        try:
                show = Show.objects.filter(showID = show_id)[0]
                QA1_object = show.QA1
                print('retrieved content local name is '+str(unicode(QA1_object.localized).encode('utf8')))
                return str(unicode(QA1_object.localized).encode('utf8'))
        except:
		print('exception in retrieving show localname')
                return "none"



def get_show_QA2_filepath(show_id):

        try:
                show = Show.objects.filter(showID = show_id)[0]
                QA2_object = show.QA2
                print('retrieved show details are '+str(QA2_object.file))
                return str(QA2_object.file)
        except:
                return "none"

def get_show_QA2_localname(show_id):

        try:
                show = Show.objects.filter(showID = show_id)[0]
                QA2_object = show.QA2
                print('retrieved show details are '+str(unicode(QA2_object.localized).encode('utf8')))
                return str(unicode(QA2_object.localized).encode('utf8'))
        except:
                return "none"



def get_show_question2_filepath(show_id):

        try:
                show = Show.objects.filter(showID = show_id)[0]
                question2_filepath = show.question2
                print('retrieved show details are '+str(question2_filepath))
                return str(question2_filepath)
        except:
                return "none"


def get_show_answer2_filepath(show_id):

        try:
                show = Show.objects.filter(showID = show_id)[0]
                answer2_filepath = show.answer2
                print('retrieved show details are '+str(answer2_filepath))
                return str(answer2_filepath)
        except:
                return "none"


def get_show_question3_filepath(show_id):

        try:
                show = Show.objects.filter(showID = show_id)[0]
                question3_filepath = show.question3
                print('retrieved show details are '+str(question3_filepath))
                return str(question3_filepath)
        except:
                return "none"

def get_show_answer3_filepath(show_id):

        try:
                show = Show.objects.filter(showID = show_id)[0]
                answer3_filepath = show.answer3
                print('retrieved show details are '+str(answer3_filepath))
                return str(answer3_filepath)
        except:
                return "none"



#function updates show statistics at the portal side, this function needs to be called from somewhere, right now using this file only
def update_show_stats_in_portal(show_id):
	recording_dir = fs_config.recording_dir + show_id + "/"
	show = Show.objects.filter(showID = show_id)[0]

	zipfile_name = show_id + '_stats.zip'
	file_path = recording_dir + zipfile_name
	show = Show.objects.filter(showID = show_id)[0]
	

	with zipfile.ZipFile(file_path, mode='w') as zf:
		for dir in os.listdir(str(recording_dir)):
			print("dir", str(dir))
			if os.path.isdir(str(recording_dir)+dir):
				for file_name in os.listdir(str(recording_dir)+dir):
					print('file is ', file_name)
					if ".csv" in file_name:
                                		print('found csv')
						try:
							print("writing")
                                			zf.write(recording_dir+dir+"/"+file_name,  arcname = file_name)
							#zf.write(file_name)
						except:
							print("exception")
							#zf.close()
			else:
				print('not a directory')
		zf.close()
	
	with open(file_path, 'rb') as stats_file:
		show.show_stats.save(zipfile_name, File(stats_file), save = True)
	
        return True


#update_show_stats_in_portal('show_15')
#get_show_question1_filepath('show_19')
q1 = get_show_QA2_filepath('show_22')
print('q1 is '+q1)
ql = get_show_QA2_localname('show_22')
print(ql)
