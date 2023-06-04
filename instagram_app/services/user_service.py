from rest_framework.exceptions import ValidationError

from instagram_app.repositories.user_repository import UserRepository
from instagram_app.serializers import UserSerializer


class UserService:
    def __init__(self):
        self._repository = UserRepository()

    def login(self, data: dict) -> dict:
        user, token = self._repository.get_token(data)
        return {"user": UserSerializer(user).data, "token": token.key}

    def get_users(self, data: dict = None):
        if data.get('search'):
            return self._repository.get_users_by_name(data.get('search'))
        return self._repository.get_users()

    def get_following_users(self, user_id):
        return self._repository.get_following(user_id)

    def get_current_user(self, key: str):
        user = self._repository.get_current_user(key)
        if not user:
            raise ValidationError()
        return user

    def get_user_by_param(self, data: dict):
        if not data: return
        value = ''
        if data.get('email'):
            value = data.get('email')
        return self._repository.get_user_with_filter(value)

    def send_reset_password_email(self, user_id: int):
        ...

