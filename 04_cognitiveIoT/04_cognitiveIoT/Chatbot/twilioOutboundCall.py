# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
# from twilio.twiml.voice_response import Dial, VoiceResponse, Sip
# from twilio.twiml.voice_response import Dial, VoiceResponse, Say


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACbcb566aa564562f095099114d9a9b81d'
auth_token = '8fb8e6d9653d15bed0bf033e3f9531bc'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        # url='http://demo.twilio.com/docs/voice.xml',
                        url='https://arsenic-peafowl-3712.twil.io/parse-digits',
                        # https://handler.twilio.com/twiml/EH99b369c8626fbb359e3d67beb8a87564
                        to='+919873093554',
                        from_='+12057076915'
                        
                        # body='Hello from Python! you recieve this call from Vishnu Nahak'
                    )
# print(response)


print("Call SID = ", call.sid)                    

# response = VoiceResponse()
# dial = Dial()
# dial.sip(
#     'sip:kate@example.com',
#     status_callback_event='initiated ringing answered completed',
#     status_callback='https://myapp.com/calls/events',
#     status_callback_method='POST'
# )
# response.append(dial)

# print(response)


# print("Call SID = ", call.sid)
# message = client.messages.create(
#     to="+919873093554", 
#     from_="+13343162433",
#     body="Hello from Vishnu Nahak! you recieve this call from Vishnu Nahak have a great day!!")

# print("Message SID = ", message.sid)



# response = VoiceResponse()
# response.dial('+919873093554')
# response.say('Goodbye')

# print(response)


# from twilio.twiml.voice_response import VoiceResponse, Say

# response = VoiceResponse()
# say = Say('Hi', voice='Polly.Joanna')
# say.ssml_break(strength='x-weak', time='100ms')
# say.ssml_emphasis('Words to emphasize', level='moderate')
# say.ssml_p('Words to speak')
# say.append('aaaaaa')
# say.ssml_phoneme('Words to speak', alphabet='x-sampa', ph='pɪˈkɑːn')
# say.append('bbbbbbb')
# say.ssml_prosody('Words to speak', pitch='-10%', rate='85%', volume='-6dB')
# say.ssml_s('Words to speak')
# say.ssml_say_as('Words to speak', interpret_as='spell-out')
# say.ssml_sub('Words to be substituted', alias='alias')
# say.ssml_w('Words to speak')
# response.append(say)

# print(response)


