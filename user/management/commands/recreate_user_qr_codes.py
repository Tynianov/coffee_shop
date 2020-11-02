from django.core.management.base import BaseCommand

from user.models import User
from qr_code.utils import recreate_model_qr_code


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                recreate_model_qr_code(user)
                print(f'QR code successfully recreated for user with id {user.id}')
            except Exception as e:
                print(f'Error occurred while updating qr code for user {user.id}, {e}')
