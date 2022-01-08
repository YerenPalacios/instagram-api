from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from instagram_app.serializers import CommentSerializer, CommentViewSerializer


class CommentView(ListCreateAPIView):
    serializer_class = CommentViewSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def list(self, request):
        query = self.queryset.filter(user = request.user)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data)

    def create(self, request):
        print(request.data)
        data = {
            'post':request.data.get('post'),
            'text':request.data.get('text'),
            'user':request.user.id
        }
        serializer = self.serializer_class(data=data, context=data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response({
            'comments':CommentSerializer(
                comment.post.comments.all(), many=True
            ).data
        })