from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from instagram_app.serializers import CommentSerializer, CommentViewSerializer
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
        print(request.data)
        data = {
            'post': request.data.get('post'),
            'text': request.data.get('text'),
            'user': request.user.id
        }
        serializer = self.serializer_class(data=data, context=data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response({
            'comments': CommentSerializer(
                comment.post.comments.all(), many=True
            ).data
        })
