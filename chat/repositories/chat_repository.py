from django.db.models import QuerySet

from chat.models import ChatRoomMessage


class ChatRepository:
    @staticmethod
    def get_messages_by_room(room_id: str) -> QuerySet[ChatRoomMessage]:
        return ChatRoomMessage.objects.filter(room_id=room_id)

    @staticmethod
    def create_message(user_id: int, room_id: int, content: str) -> ChatRoomMessage:
        return ChatRoomMessage.objects.create(user_id=user_id, room_id=room_id, content=content)
