from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

from voucher.models import VoucherConfig
from voucher.serializers import VoucherConfigSerializer

from .serializers import \
    UserSerializer,\
    ValidateUserQrCodeSerializer,\
    PasswordResetBySMSSerializer, \
    ValidatePasswordResetPasswordCodeSerializer, \
    ChangePasswordSerializer


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScanUserQRCodeView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):

        user_id = self.kwargs.get("pk")
        serializer = ValidateUserQrCodeSerializer(data={"id": user_id, "initiator": request.user})
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


class RequestPasswordRestCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetBySMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'data': _("Code was successfully send by SMS")})


class ValidatePasswordResetPasswordCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ValidatePasswordResetPasswordCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        return Response({'key': user.auth_token.key})


class ChangePasswordView(ModelViewSet):
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):

        user = request.user
        serializer = self.get_serializer(data=request.data, context={'user': user})

        if serializer.is_valid():
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response(data={'message': _('Password was successfully changed')}, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
