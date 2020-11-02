from django.core.management.base import BaseCommand

from voucher.models import Voucher
from qr_code.utils import recreate_model_qr_code


class Command(BaseCommand):
    def handle(self, *args, **options):
        for voucher in Voucher.objects.not_scanned():
            try:
                recreate_model_qr_code(voucher)
                print(f'QR code successfully recreated for voucher with id {voucher.id}')
            except Exception as e:
                print(f'Error occurred while updating qr code for user {voucher.id}, {e}')
