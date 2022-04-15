from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from django.db.models import Q, OuterRef
from rest_framework.response import Response
from instagram_app.serializers.message import MessageSerializer
from instagram_app.serializers.user import UserChattingSerializer, UserSerializer


class MessageView(ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(
            Q(user=self.request.user) & Q(send_to=self.request.GET['send_to']) |
            Q(user=self.request.GET['send_to']) & Q(send_to=self.request.user)
        ).order_by('created_at')

    def create(self, request):
        model = self.serializer_class.Meta.model
        model.objects.create(
            text=request.data['text'],
            user_id=request.user.id,
            send_to_id=request.GET['send_to']
        )
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=201)


class ChatListView(APIView):

    def get(self, request):
        qs = request.user.message_set.distinct('send_to')
        data = [
            UserChattingSerializer(i.send_to, context={"user": request.user}).data for i in qs
        ]
        return Response(data)
