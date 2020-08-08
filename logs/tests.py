from mixer.backend.django import mixer

from utils.conftest import BaseTestCase
from voucher.models import Voucher
from user.models import User
from qr_code.models import UserQRCode

from .models import ScanLogEntry


class TestScanUserQRCode(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.url = '/api/v1/user/scan-qr-code/'

