from instagram_app.repositories.user_repository import UserRepository
from instagram_app.serializers import UserSerializer


class UserService:
    def __init__(self):
        self._repository = UserRepository()

    def login(self, data: dict) -> dict:
        user, token = self._repository.get_token(data)
        return {"user": UserSerializer(user).data, "token": token.key}

    def get_following_users(self, user_id):
        return self._repository.get_following(user_id)
