from chat.models import *
from rest_framework.generics import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from django.db.models import Q, Count
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model as User

from chat.services.chat_service import ChatService
from instagram_app.serializers.message import MessageSerializer
from instagram_app.serializers.user import UserChattingSerializer, ChatSerializer


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


class ChatListView(ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)
    service = ChatService()

    def create(self, request, *args, **kwargs):
        user = self.request.auth.user
        chatting_user = get_object_or_404(
            User(), username=request.data.get('username'))
        users = [user, chatting_user]

        created_room = self.request.auth.user.chatroom_set.annotate(
            users_count=Count('users')
        ).filter(users_count=2, users__in=users)

        if not created_room:
            room = ChatRoom.objects.create()
            room.users.set(users)
            room.save()

        return Response({}, status=201)

    def get(self, request, *args, **kwargs):
        rooms = self.service.get_chat_rooms(request.user.id)
        return Response(self.serializer_class(rooms, many=True).data)
