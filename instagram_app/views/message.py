from rest_framework.generics import ListCreateAPIView
from instagram_app.serializers.message import MessageSerializer

class MessageView(ListCreateAPIView):
    serializer_class = MessageSerializer
    queryset = serializer_class.Meta.model.objects.all()