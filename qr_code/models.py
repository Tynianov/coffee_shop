import qrcode
from io import BytesIO

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import ugettext_lazy as _

from user.models import User
from voucher.models import Voucher


class QRCode(models.Model):
    """
    Default QR code class
    """

    qr_code = models.ImageField(
        _("QR code"), upload_to="qr_codes", blank=True, null=True
    )

    class Meta:
        abstract = True

    def create_code(self, data, filename=None):
        """
        Create the QR Code
        data - data that needs to be encoded in the qr image
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        filename = f"{filename or str(self.pk)}.png"
        file_buffer = InMemoryUploadedFile(
            buffer, None, filename, "image/png", len(buffer.getvalue()), None
        )
        self.qr_code.save(filename, file_buffer)


class UserQRCode(QRCode):
    """
    Staff qr code
    """

    user = models.OneToOneField(
        User,
        verbose_name=_("User"),
        related_name="qr_code",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} QR code [{self.pk}]"

    class Meta:
        verbose_name = _("User QR code")
        verbose_name_plural = _("User QR codes")


class VoucherQRCode(QRCode):
    voucher = models.OneToOneField(
        Voucher,
        verbose_name=_("Voucher"),
        related_name="qr_code",
        on_delete=models.CASCADE,
    )
    qr_code = models.ImageField(
        _("QR Code"), upload_to="vouchers/qr_codes", blank=True, null=True
    )

    def __str__(self):
        return f"{self.voucher} QR code [{self.pk}]"

    class Meta:
        verbose_name = _("Voucher QR code")
        verbose_name_plural = _("Voucher QR code")
