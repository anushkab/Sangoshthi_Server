# These details are used by the program to connect remotely via ESL to Freeswitch,
# enables us to execute commands and listen to events.
#password= 'PASSWORD'
password= 'ClueCon'
server ='0.0.0.0'
port = '8022'
# The Sip provider's configuration file should be saved as an XML file in the
# FREESWITCH_DIR/sip_profiles/external folder
gateway = 'sofia/gateway/MySIP/'
# a Telephone number bought from the SIP provider so that outgoing calls from the server are mapped to a fixed number
# on the participant's device. If no number is provided, when host/listener is called, call will appear as
# Unknown/Withheld/Private on the user's call screen
sip_phone_number = 'PHONE_NUMBER'