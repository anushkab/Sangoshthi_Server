
from pydub import AudioSegment
import fs_config 
import os

def combine_show_recordings(show_id, output_location, input_recording_paths):
	recording_dir = "/home/sangoshthi"
	count = len(input_recording_paths)
	print("number of recordings", str(count))
	flag = 1
	for recording in input_recording_paths:
		if flag == 1:
			combined_sound = AudioSegment.from_wav(recording)
		else:
			combined_sound += AudioSegment.from_wav(recording)

        try:
                output_file = str(output_location+show_id+"_"+"combined_recording.wav")
                print("output file is ", output_file)
                ret_value = combined_sound.export(output_file, format="wav")
        except:
                print("error occurred in combining the recordings of show",show_id)



recordings = []
recordings.append(str(fs_config.recording_dir + "show_1/show_1_2017_06_11_15_14_49/show_1_2017_06_11_15_14_49.wav"))
recordings.append(str(fs_config.recording_dir + "show_1/show_1_2017_06_15_10_39_21/show_1_2017_06_15_10_39_21.wav"))
print(str(recordings))
combine_show_recordings("show_1", recordings)



"""
#flag = 1
def concaenate_conference_recordings(show_id):

	recording_dir = fs_config.recording_dir + show_id
	flag = 1

	for dir in os.listdir(str(recording_dir)):
		print("dir", str(dir))
		for recording_file in os.listdir(str(recording_dir)+"/"+dir):
			print("level1",recording_file)
			if ".wav" in recording_file:
				print(recording_file)
				if flag == 1 :
					combined_sound = AudioSegment.from_wav(str(recording_dir+"/"+dir+"/"+recording_file))
					flag = flag + 1
				else:
					combined_sound += AudioSegment.from_wav(str(recording_dir+"/"+dir+"/"+recording_file))
					print(combined_sound)
	try:
		output_file = str(recording_dir+"/"+show_id+"_"+"combined_recording.wav")
		print("output file is ", output_file)
		ret_value = combined_sound.export(output_file, format="wav")
	except:
		print("error occurred in combining the recordings of show",show_id)
	flag = 1


concaenate_conference_recordings("show_1")
"""


#for root, dirs, files in os.walk(recording_dir):
#    print(dirs)
#    path = root.split(os.sep)
#    depth = root[len(path) + len(os.path.sep):].count(os.path.sep)
#    if depth == 3:
#    print((len(path) - 1) * '---', os.path.basename(root))
#    for file in files:
#        print(len(path) * '---', file)

"""

sound1 = AudioSegment.from_wav("/home/sangoshthi/sangoshthi_new/topic.wav")
sound2 = AudioSegment.from_wav("/home/sangoshthi/sangoshthi_new/welcome.wav")

combined_sounds = sound1 + sound2
combined_sounds.export("/home/sangoshthi/sangoshthi_new/output.wav", format="wav")
"""
