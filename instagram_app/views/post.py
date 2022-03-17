import base64
import io
import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import SuspiciousOperation

from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from instagram_app.models import Images, Comment, Like
from instagram_app.serializers import PostSerializer




# WARNING: quick and dirty, should be used for reference only.

def to_file(file_from_POST):
    """base64 encoded file to Django InMemoryUploadedFile that can be placed into request.FILES."""
    # 'data:image/png;base64,<base64 encoded string>'
    try:
        idx = file_from_POST[:50].find(',')  # comma should be pretty early on

        if not idx or not file_from_POST.startswith('data:image/'):
            raise Exception()

        base64file = file_from_POST[idx+1:]
        attributes = file_from_POST[:idx]
        content_type = attributes[len('data:'):attributes.find(';')]
    except Exception as e:
        raise SuspiciousOperation("Invalid picture")

    f = io.BytesIO(base64.b64decode(base64file))
    ext = content_type.split('/')[1]
    image = InMemoryUploadedFile(f,
       field_name='picture',
       name='picture.'+ext,  # use UUIDv4 or something
       content_type=content_type,
       size=sys.getsizeof(f),
       charset=None)
    return image

  
class PostsView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = self.serializer_class.Meta.model.objects.prefetch_related(
            Prefetch('likes', queryset=Like.objects.filter(user=self.request.user)), 
            Prefetch(
                'comments',
                queryset=Comment.objects.filter(
                    user=self.request.user
                ).select_related('user')
            ),
            'images'
        ).order_by('-created_at')
        return queryset

    def get_serializer_context(self):
        context = super(PostsView, self).get_serializer_context()
        context.update({'user' : self.request.user})
        return context

    def post(self, request, format=None):
        model = self.serializer_class.Meta.model
        post = model.objects.create(
            user=self.request.user,
            text=self.request.data.get('text')
        )
        images = request.data.get('images', [])

        if len(images) > 0:
            for image in images:
                Images.objects.create(image=to_file(image), post=post)

        post = self.serializer_class(post).data

        return Response(post, status=201)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = serializer_class.Meta.model.objects.select_related(
        'user'
    ).prefetch_related('images', 'comments', 'likes')