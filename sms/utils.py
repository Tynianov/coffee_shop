from twilio.rest import Client
from django.conf import settings

twilio_client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)


def twilio_send_sms(to, message):
    twilio_client.messages.create(
        to=to,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message
    )
