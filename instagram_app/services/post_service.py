from chat.repositories.chat_repository import ChatRepository
from instagram_app.repositories.post_repository import PostRepository


class PostService:
    def __init__(self):
        self._repository = PostRepository()
        self.chat_repository = ChatRepository()

    def get_posts(self, limit=0, offset=0, user_id: int = None, **kwargs):
        if user_id:
            return self._repository.get_posts_for_user(user_id, limit, offset, **kwargs)
        return self._repository.get_general_posts(limit, offset)

    def share_post(self, post_id: int, text: str, chat_room_id: int, from_user: int):
        self.chat_repository.create_message(room_id=chat_room_id, user_id=from_user, content=str(post_id), is_post=True)
        if text != '':
            self.chat_repository.create_message(room_id=chat_room_id, user_id=from_user, content=text)

    def get_post(self, post_id: int):
        return self._repository.get_post(post_id)
