from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from django.db.models import Q, OuterRef, Prefetch,Count
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

from chat.models import * 

class ChatListView(APIView):

    def get(self, request):
        rooms = ChatRoom.objects.annotate(users_count=Count('users')).filter(users_count=2, users=request.user)
        
        data = UserChattingSerializer(rooms,many=True, context={"user": request.user}).data
        return Response(data)
