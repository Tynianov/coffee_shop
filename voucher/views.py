from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.utils.translation import ugettext_lazy as _

from .serializers import ScanVoucherSerializer, VoucherSerializer


class ScanVoucherQRCode(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        voucher_id = self.kwargs.get('pk')
        serializer = ScanVoucherSerializer(data={"id": voucher_id})
        if serializer.is_valid():
            data = {
                'message': _("QR Code scanned successfully"),
                'voucher': VoucherSerializer(serializer.voucher).data
            }
            return Response(data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
