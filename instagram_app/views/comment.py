from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from instagram_app.serializers import CommentViewSerializer
from instagram_app.services.comment_service import CommentService


# TODO: add test
class CommentView(ListCreateAPIView):
    serializer_class = CommentViewSerializer
    queryset = serializer_class.Meta.model.objects.all()
    service = CommentService()

    def list(self, request, *args):
        data = self.service.get_post_comments(request.GET.get('post'))
        return Response(data)

    def create(self, request, *args):
        data = {
            'post': request.data.get('post'),
            'text': request.data.get('text'),
            'user': request.user.id
        }
        return Response(self.service.create_comment(data))
