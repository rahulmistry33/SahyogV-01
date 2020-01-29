from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
def makeCall():
    account_sid = 'ACc4b67eb6c1d521f75d927122e60e1719'
    auth_token = 'b541bf5e349b93c95d0e1556bc77b2ba'
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            twiml='<Response><Say>Gayatri has pressed SOS button at KJ Somaiya College Of Engineering,VidyaVihar East.</Say></Response>',
                            to='+918879272265',
                            from_='+12566702823'
                        )

    return call