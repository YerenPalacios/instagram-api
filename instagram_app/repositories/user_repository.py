from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from instagram_app.models import User


class UserRepository:
    @staticmethod
    def authenticate(data: dict) -> User:
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError({"error": "Invalid username or password"})
        return user

    def get_token(self, data: dict) -> [User, Token]:
        user = self.authenticate(data)
        token, created = Token.objects.get_or_create(user=user)
        return user, token

    @staticmethod
    def get_following(user_id: int):
        return User.objects.filter(following__follower_id=user_id)
