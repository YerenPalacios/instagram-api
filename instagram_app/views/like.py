from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from instagram_app.serializers import LikeSerializer


class LikeView(ListCreateAPIView):
    serializer_class = LikeSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def create(self, request):
        print(request.data)
        data = {
            'post':request.data.get('post'),
            'user':request.user.id
        }
        serializer = self.serializer_class(data=data, context=data)
        serializer.is_valid(raise_exception=True)
        if serializer.save():
            return Response({'liked':True})
        return Response({'liked':False})
