from typing import List

from django.db.models import QuerySet, Count, Prefetch, Subquery, OuterRef

from chat.models import ChatRoomMessage, ChatRoom
from instagram_app.models import User


class ChatRepository:
    @staticmethod
    def get_messages_by_room(room_id: int) -> QuerySet[ChatRoomMessage]:
        return ChatRoomMessage.objects.filter(room_id=room_id)

    @staticmethod
    def create_message(user_id: int, room_id: int, content: str, **kwargs) -> ChatRoomMessage:
        return ChatRoomMessage.objects.create(user_id=user_id, room_id=room_id, content=content, **kwargs)

    def get_chat_room(self, chat_room_id: int) -> ChatRoom:
        return ChatRoom.objects.get(id=chat_room_id)

    def get_chat_rooms(self, user_id) -> QuerySet[ChatRoom]:
        last_message_qs = ChatRoomMessage.objects.filter(room_id=OuterRef('id'))
        rooms = ChatRoom.objects.prefetch_related(
            Prefetch('users', queryset=User.objects.exclude(id=user_id)),
        ).annotate(
            users_count=Count('users'),
            last_message_id=Subquery(last_message_qs.values('id')[:1]),
            timestamp=Subquery(last_message_qs.values('timestamp')[:1]),
            content=Subquery(last_message_qs.values('content')[:1]),
            is_post=Subquery(last_message_qs.values('is_post')[:1]),
            user_id=Subquery(last_message_qs.values('user_id')[:1]),
            room_id=Subquery(last_message_qs.values('room_id')[:1]),

        ).filter(users_count=2, users__id=user_id)
        return rooms
