from chat.repositories.chat_repository import ChatRepository
from instagram_app.serializers import ChatRoomMessageSerializer


class ChatService:
    def __init__(self):
        self.repository = ChatRepository()
        self.serializer = ChatRoomMessageSerializer

    def get_messages_by_room(self, room_id: int) -> list:
        messages = self.repository.get_messages_by_room(room_id)
        return self.serializer(messages, many=True).data

    def create_message(self, user_id, room_id, content) -> dict:
        message = self.repository.create_message(user_id, room_id, content)
        return ChatRoomMessageSerializer(message).data
