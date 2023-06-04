from instagram_app.repositories.post_repository import PostRepository


class PostService:
    def __init__(self):
        self._repository = PostRepository()

    def get_posts(self, limit=0, offset=0, user_id: int = None, priority: bool = None):
        if user_id:
            return self._repository.get_posts_for_user(user_id, priority, limit, offset)
        return self._repository.get_general_posts(limit, offset)
