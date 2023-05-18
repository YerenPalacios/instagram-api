from django.urls import reverse
from django_dynamic_fixture import G
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from instagram_app.models import User
from instagram_app.views.user import LoginView


class UserApiTestCase(APITestCase):
    user_email = 'test_user@test.test'

    @classmethod
    def setUpTestData(cls):
        cls.user: User = G(User, email=cls.user_email)
        cls.user.set_password('test_pass')
        cls.user.save()
        cls.url = reverse(LoginView.name)

    def test_login(self):
        payload = {
            "email": self.user_email,
            "password": "test_pass"
        }
        res = self.client.post(self.url, data=payload)
        self.assertEqual(res.status_code, 201)
        token = Token.objects.get(user__email=self.user_email)
        self.assertEqual(res.data["token"], token.key)

    def test_invalid_login(self):
        payload = {
            "email": self.user_email,
            "password": "invalid_pass"
        }
        res = self.client.post(self.url, data=payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), {"error": "Invalid username or password"})
