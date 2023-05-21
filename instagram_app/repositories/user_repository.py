from django.contrib.auth import authenticate
from django.db.models import QuerySet, Q
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

    def get_current_user(self, key: str) -> User:
        token = Token.objects.filter(key=key)
        if token:
            return token[0].user

    @staticmethod
    def get_users():
        return User.objects.all()

    def get_following(self, user_id: int):
        return self.get_users().filter(following__follower_id=user_id)

    def get_following_user_ids(self, user_id: int) -> list:
        return self.get_following(user_id).values_list('id')

    def get_users_by_name(self, name) -> QuerySet[User]:
        return self.get_users().filter(Q(name__icontains=name) | Q(username__icontains=name))[:10]
