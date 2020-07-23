from rest_framework import status
from rest_framework.views import APIView
from rest_auth.registration.views import RegisterView
from rest_framework.response import Response

from .serializers import CustomRegistrationSerializer, UserSerializer


class CustomRegistrationView(RegisterView):
    serializer_class = CustomRegistrationSerializer


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
