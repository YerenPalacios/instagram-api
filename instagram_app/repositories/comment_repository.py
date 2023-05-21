from django.db.models import QuerySet

from instagram_app.models import Comment


class CommentRepository:
    @staticmethod
    def get_comments_by_post(post_id: int) -> QuerySet[Comment]:
        return Comment.objects.filter(post_id=post_id)

    @staticmethod
    def create_post_comment(post_id: int, user_id: int, content: str) -> Comment:
        return Comment.objects.create(post_id=post_id, user_id=user_id, text=content)
