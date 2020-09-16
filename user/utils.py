import logging
from django.conf import settings
from fcm_django.models import FCMDevice


logger = logging.getLogger('db')


def send_push_notification(user, title, data):
    if not settings.FCM_SERVER_KEY:
        logger.error("No FCM key specified")
        return

    device = FCMDevice.objects.filter(user=user).first()

    if not device:
        logger.error(f"Device not found. User id: {user.id}")
        return

    message_data = {
        'title': title,
        'data': data,
        'api_key': settings.FCM_SERVER_KEY,
        'click_action': 'FLUTTER_NOTIFICATION_CLICK'
    }

    device.send_message(**message_data)
    logger.warning("Push send")
    return
