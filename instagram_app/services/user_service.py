from rest_framework.exceptions import ValidationError

from instagram_app.repositories.user_repository import UserRepository
from instagram_app.serializers import UserSerializer
from instagram_app.utils import generate_random_color


class UserService:
    def __init__(self):
        self._repository = UserRepository()

    def login(self, data: dict) -> dict:
        return self._repository.get_token(data)

    def get_users(self, data: dict = None, limit: int = None, auth_user_id: int = None):
        if data.get('search'):
            return self._repository.get_users_by_name(data.get('search'), auth_user_id)
        users = self._repository.get_users(auth_user_id)
        if limit:
            return users[:limit]
        return users

    def get_following_users(self, user_id):
        return self._repository.get_following(user_id)

    def get_current_user(self, key: str):
        user = self._repository.get_current_user(key)
        if not user:
            raise ValidationError()
        return user

    def get_user_exists(self, value: str):
        return {"exists": self._repository.get_user_exists(value)}

    def create_user(self, data: dict):
        return self._repository.create_user(data)
