from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView

from instagram_app.models import Images, Comment, Like
from instagram_app.serializers import PostSerializer


class PostsView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = self.serializer_class.Meta.model.objects.exclude(
            user = self.request.user
        ).prefetch_related(
            Prefetch('likes', queryset=Like.objects.filter(user=self.request.user)), 
            Prefetch(
                'comments',
                queryset=Comment.objects.filter(
                    user=self.request.user
                ).select_related('user')
            ),
            'images'
        )
        return queryset

    def get_serializer_context(self):
        context = super(PostsView, self).get_serializer_context()
        context.update({'user' : self.request.user})
        return context

    def create(self, request):
        model = self.serializer_class.Meta.model
        post = model.objects.create(
            user=self.request.user,
            text=self.request.data['text']
        )
        images = request.data.get('images', [])
        if len(images) > 0:
            for image in images:
                Images.objects.create(image=image, user=self.request.user)

        post = self.serializer_class(post).data

        return Response(post, status=201)