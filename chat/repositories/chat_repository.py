from typing import List

from django.db.models import QuerySet, Count

from chat.models import ChatRoomMessage, ChatRoom


class ChatRepository:
    @staticmethod
    def get_messages_by_room(room_id: str) -> QuerySet[ChatRoomMessage]:
        return ChatRoomMessage.objects.filter(room_id=room_id)

    @staticmethod
    def create_message(user_id: int, room_id: int, content: str, **kwargs) -> ChatRoomMessage:
        return ChatRoomMessage.objects.create(user_id=user_id, room_id=room_id, content=content, **kwargs)

    def get_chat_room(self, chat_room_id: int) -> ChatRoom:
        return ChatRoom.objects.get(id=chat_room_id)
