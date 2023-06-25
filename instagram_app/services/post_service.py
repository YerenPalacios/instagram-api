from chat.repositories.chat_repository import ChatRepository
from instagram_app.helpers import generate_thumbnail
from instagram_app.repositories.post_repository import PostRepository


class PostService:
    def __init__(self):
        self._repository = PostRepository()
        self.chat_repository = ChatRepository()

    @staticmethod
    def _add_thumbnail(post):
        for file in post.files.all():
            if file.file.name.endswith('.mp4'):
                file.thumbnail = generate_thumbnail(file.file.path)

    def get_posts(self, limit=0, offset=0, user_id: int = None, **kwargs):
        if user_id:
            posts = self._repository.get_posts_for_user(user_id, limit, offset, **kwargs)
        else:
            posts = self._repository.get_general_posts(limit, offset)
        for post in posts:
            self._add_thumbnail(post)
        return posts

    def share_post(self, post_id: int, text: str, chat_room_id: int, from_user: int):
        self.chat_repository.create_message(room_id=chat_room_id, user_id=from_user, content=str(post_id), is_post=True)
        if text != '':
            self.chat_repository.create_message(room_id=chat_room_id, user_id=from_user, content=text)

    def get_post(self, post_id: int):
        post = self._repository.get_post(post_id)
        self._add_thumbnail(post)
        return post
