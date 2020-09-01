from json import dumps
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from user.models import User


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.user = mixer.blend(User)
        self.token = Token.objects.create(user=self.user)
        self.superuser = mixer.blend(User, is_superuser=True)
        self.superuser_token = Token.objects.create(user=self.superuser)
        self.api_client = APIClient()

    def json_post_request(self, path, data):
        return self.api_client.post(path=path,
                                    data=dumps(data),
                                    content_type='application/json')

    def set_token(self, token):
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def incorrect_token(self):
        self.api_client.credentials(HTTP_AUTHORIZATION='Token definitely correct token')
