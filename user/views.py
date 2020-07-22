from rest_auth.registration.views import RegisterView
from rest_framework.authentication import TokenAuthentication
from rest_auth.registration.views import LoginView

from .serializers import CustomRegistrationSerializer


class CustomRegistrationView(RegisterView):
    serializer_class = CustomRegistrationSerializer


class CustomLoginView(LoginView):
    authentication_classes = [TokenAuthentication]
