from instagram_app.repositories.comment_repository import CommentRepository
from instagram_app.serializers import CommentSerializer, CommentViewSerializer


class CommentService:

    def __init__(self):
        self._repository = CommentRepository()

    def get_post_comments(self, post_id: int):
        comments = self._repository.get_comments_by_post(post_id)
        return CommentSerializer(comments, many=True).data

    def create_comment(self, data: dict):
        serializer = CommentViewSerializer(data=data, context=data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return CommentSerializer(comment).data
