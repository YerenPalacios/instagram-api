import base64
import io
import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import SuspiciousOperation
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView

from instagram_app.models import Files
from instagram_app.serializers import PostSerializer
from instagram_app.services.post_service import PostService


# WARNING: quick and dirty, should be used for reference only.

def to_file(file_from_POST):
    """base64 encoded file to Django InMemoryUploadedFile that can be placed into request.FILES."""
    # 'data:image/png;base64,<base64 encoded string>'
    try:
        idx = file_from_POST[:50].find(',')  # comma should be pretty early on

        if not idx or not file_from_POST.startswith('data:image/'):
            raise Exception()

        base64file = file_from_POST[idx + 1:]
        attributes = file_from_POST[:idx]
        content_type = attributes[len('data:'):attributes.find(';')]
    except Exception as e:
        raise SuspiciousOperation("Invalid picture")

    f = io.BytesIO(base64.b64decode(base64file))
    ext = content_type.split('/')[1]
    image = InMemoryUploadedFile(
        f,
        field_name='picture',
        name='picture.' + ext,  # use UUIDv4 or something
        content_type=content_type,
        size=sys.getsizeof(f),
        charset=None)
    return image


DEFAULT_LIMIT = 5
DEFAULT_OFFSET = 0


def get_filters(params: dict) -> dict:
    filters = {}
    for key in params.keys():
        if params.get(key) in ['true', 'false']:
            filters[key] = bool(params.get(key))
        else:
            filters[key] = params.get(key)
    return filters


class PostsView(ListCreateAPIView):
    name = "posts"
    serializer_class = PostSerializer
    service = PostService()

    def get_queryset(self):
        user = self.request.user
        params = get_filters(self.request.GET)
        limit = int(params.pop('limit', DEFAULT_LIMIT)) or DEFAULT_LIMIT
        offset = int(params.pop('offset', DEFAULT_OFFSET)) or DEFAULT_OFFSET
        user_id = user.id if user.is_authenticated else None
        return self.service.get_posts(limit, offset, user_id, **params)

    def get_serializer_context(self):
        context = super(PostsView, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context

    def post(self, request, *args):
        model = self.serializer_class.Meta.model
        post = model.objects.create(
            user=self.request.user,
            text=self.request.data.get('text')
        )
        files = request.data.get('files', [])

        if len(files) > 0:
            for file in files:
                Files.objects.create(file=to_file(file), post=post)

        post.likes_count = 0
        post.last_owner_comment = 0
        post.comments_count = 0

        post = self.get_serializer(post).data

        return Response(post, status=201)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    service = PostService()
    queryset = serializer_class.Meta.model.objects.select_related(
        'user'
    ).prefetch_related('images', 'comments', 'likes')

    def get_object(self):
        return self.service.get_post(self.kwargs['pk'])


class SharePostSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    post_id = serializers.IntegerField()
    text = serializers.CharField(allow_blank=True)


class SharePostView(GenericAPIView):
    name = 'share_post_view'
    path = 'share-post/'
    service = PostService()

    def post(self, request):
        serializer = SharePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.share_post(**serializer.data, from_user=request.auth.user.id)
        return Response('Ok')
