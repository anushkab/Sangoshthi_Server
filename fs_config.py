# These details are used by the program to connect remotely via ESL to Freeswitch,
# enables us to execute commands and listen to events.
#password= 'PASSWORD'
password= 'ClueCon'
server ='0.0.0.0'
port = '8022'
# The Sip provider's configuration file should be saved as an XML file in the
# FREESWITCH_DIR/sip_profiles/external folder
gateway_doorvaani = 'sofia/gateway/MySIP/'
gateway_ip = '192.168.2.69'
# a Telephone number bought from the SIP provider so that outgoing calls from the server are mapped to a fixed number
# on the participant's device. If no number is provided, when host/listener is called, call will appear as
# Unknown/Withheld/Private on the user's call screen
sip_phone_number = 'PHONE_NUMBER'
base_dir = '/home/sangoshthi/sangoshthi_new/'
recording_dir = '/home/sangoshthi/sangoshthi_new/recordings/'
locale = '91'
sql_host = 'localhost'
sql_user = 'root'
sql_pass = 'root'
portal_db = 'Sangoshti_Django'
recording_file_extension = '.wav'
content_base_dir = '/home/sangoshthi/tushar/Django/Sangoshti/'
port_audio_base_dir = '/home/sangoshthi/tushar/Django/Sangoshti/'
host_call_drop = '/home/sangoshthi/sangoshthi_new/sounds/wait_for_host.wav'
host_redial_timeout = '/home/sangoshthi/sangoshthi_new/sounds/host_redial_timeout.wav'
no_of_QAs_per_show = '3'
