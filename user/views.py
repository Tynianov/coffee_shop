from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

from voucher.models import VoucherConfig
from voucher.serializers import VoucherConfigSerializer
from qr_code.utils import recreate_model_qr_code

from .models import User
from .serializers import \
    UserSerializer,\
    ValidateUserQrCodeSerializer,\
    PasswordResetBySMSSerializer, \
    ValidatePasswordResetPasswordCodeSerializer, \
    ChangePasswordSerializer,\
    CompleteRegistrationSerializer


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScanUserQRCodeView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):

        user_id = self.kwargs.get("pk")
        serializer = ValidateUserQrCodeSerializer(data={"id": user_id}, context={'initiator': request.user})
        serializer.is_valid(raise_exception=True)

        if not serializer.is_voucher_received:
            return Response({"message": _("QR Code scanned successfully")})

        return Response({
            "message": _("User received voucher"),
            "voucher_name": serializer.received_voucher.voucher_config.name
        })


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


class CheckIfPhoneNumberRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', None)

        if not phone_number:
            return Response(data={
                "message": _("Phone number is missing")
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(phone_number=phone_number)
            return Response({
                "phone_number_taken": True
            })
        except User.DoesNotExist:
            return Response({
                "phone_number_taken": False
            })


class GetAuthTokenByFirebaseUid(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('firebase_uid', None)

        if not uid:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(firebase_uid=uid)
            return Response({
                "token": user.auth_token.key
            })
        except Exception:
            return Response({
                "firebase_uid": "Invalid firebase uid"
            }, status=status.HTTP_400_BAD_REQUEST)


class RecreateUserQRCodeView(APIView):
    def get(self, request):
        user = request.user
        recreate_model_qr_code(user)
        return Response(data={
            "message": _("QR code has been successfully recreated")
        })


class CompleteRegistrationView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CompleteRegistrationSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        User.objects.filter(id=obj.id).update(**data)
        return Response(data)

