from django.urls import reverse
from django_dynamic_fixture import G
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from instagram_app.models import User, Follow
from instagram_app.views.user import LoginView, ProfileStoriesView


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


class UserFollowTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(ProfileStoriesView.name)
        cls.user: User = G(User)
        cls.user_2: User = G(User)
        cls.user_3: User = G(User)
        cls.user_4: User = G(User)

        G(Follow, follower=cls.user, following=cls.user_2)
        G(Follow, follower=cls.user, following=cls.user_3)

    def test_get_users_which_are_being_followed_by_an_user(self):
        self.client.force_authenticate(self.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['id'], self.user_2.id)
        self.assertEqual(res.data[1]['id'], self.user_3.id)

    def test_get_users_which_are_being_followed_by_without_followings(self):
        self.client.force_authenticate(self.user_2)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_get_users_without_authentication(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data['detail'], "Authentication credentials were not provided.")
