from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from instagram_app.serializers import SaveSerializer


class SaveView(ListCreateAPIView):
    serializer_class = SaveSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def create(self, request):
        data = {
            'post':request.data.get('post'),
            'user':request.user.id
        }
        serializer = self.serializer_class(data=data, context=data)
        serializer.is_valid(raise_exception=True)
        if serializer.save():
            return Response({'saved':True})
        return Response({'saved':False})
