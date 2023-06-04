from django.db.models import Prefetch, QuerySet, Case, When, Q, OuterRef, Subquery, Count, Exists

from instagram_app.models import Post, Like, Comment, Save
from instagram_app.repositories.user_repository import UserRepository


class PostRepository:
    @staticmethod
    def _get_posts() -> QuerySet[Post]:
        return Post.objects.prefetch_related('images', 'user').annotate(
            comments_count=Count('comments', distinct=True),
            likes_count=Count('likes', distinct=True),
            last_owner_comment=Subquery(Comment.objects.filter(
                user=OuterRef('user'), id=OuterRef('id')
            ).order_by('-created_at').values('text')[:1])
        )

    def get_posts_for_user(self, user_id: int, priority: bool) -> QuerySet[Post]:
        following_ids = UserRepository().get_following_user_ids(user_id)
        order_fields = ['-created_at']
        posts = self._get_posts().annotate(
            is_liked=Exists(Like.objects.filter(user_id=user_id, post_id=OuterRef('id'))),
            is_saved=Exists(Save.objects.filter(user_id=user_id, post_id=OuterRef('id')))
        )

        if priority:
            order_fields = ['-priority', '-created_at']
            posts = posts.annotate(priority=Case(When(Q(user_id__in=following_ids), then=1), default=0))

        return posts.order_by(*order_fields)

    def get_general_posts(self) -> QuerySet[Post]:
        return self._get_posts().order_by('-created_at')
