from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

from voucher.models import VoucherConfig
from voucher.serializers import VoucherConfigSerializer

from .serializers import UserSerializer, ValidateUserQrCodeSerializer


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScanUserQRCodeView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):

        user_id = self.kwargs.get("pk")
        serializer = ValidateUserQrCodeSerializer(data={"id": user_id})
        serializer.is_valid(raise_exception=True)

        return Response({"message": _("QR Code scanned successfully")})


class UserVoucherDetailsView(APIView):
    def get(self, request):
        voucher_conf = VoucherConfig.objects.min_purchase_type().order_by(
            "purchase_count"
        ).first()
        if not voucher_conf:
            return Response(data={})

        voucher_conf_serializer = VoucherConfigSerializer(voucher_conf).data
        voucher_conf_serializer.update({
            "user_current_purchase_count": request.user.current_purchase_count
        })

        return Response(data=voucher_conf_serializer)
