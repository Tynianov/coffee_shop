from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

from .serializers import \
    UserSerializer,\
    ValidateUserQrCodeSerializer,\
    PasswordResetBySMSSerializer


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScanUserQRCodeView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):

        user_id = self.kwargs.get('pk')
        serializer = ValidateUserQrCodeSerializer(data={'id': user_id})
        serializer.is_valid(raise_exception=True)

        return Response({"message": _("QR Code scanned successfully")})


class PasswordResetBySMSView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetBySMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'data': _("Code was successfully send by SMS")})

