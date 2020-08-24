import nexmo
from django.conf import settings


def nexmo_client_factory():
    return nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)


def nexmo_send_sms(context):
    sms = nexmo.Sms(nexmo_client_factory())
    sms.send_message(context)
