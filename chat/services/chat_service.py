import datetime

from chat.repositories.chat_repository import ChatRepository
from instagram_app.serializers import ChatRoomMessageSerializer
from dataclasses import dataclass


@dataclass
class ChatUser:
    id: int
    last_login: datetime.datetime
    name: str
    username: str
    email: str
    phone: str
    image: str
    is_active: str
    description: str
    color: str


@dataclass
class ChatMessage:
    id: int
    timestamp: datetime.datetime
    content: str
    is_post: bool
    user_id: int
    room_id: int


@dataclass
class Chat:
    id: int
    user: ChatUser
    last_message: ChatMessage


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

    def get_chat_rooms(self, user_id: int):
        rooms = []
        db_rooms = self.repository.get_chat_rooms(user_id)
        for db_room in db_rooms:
            user = db_room.users.all()[0]
            rooms.append(Chat(
                db_room.id,
                ChatUser(
                    id=user.id,
                    last_login=user.last_login,
                    name=user.name,
                    username=user.username,
                    email=user.email,
                    phone=user.phone,
                    image=user.image.url if user.image else '',
                    is_active=user.is_active,
                    description=user.description,
                    color=user.color,
                ),
                ChatMessage(
                    id=getattr(db_room, 'last_message_id'),
                    timestamp=getattr(db_room, 'timestamp'),
                    content=getattr(db_room, 'content'),
                    is_post=getattr(db_room, 'is_post'),
                    user_id=getattr(db_room, 'user_id'),
                    room_id=getattr(db_room, 'room_id')
                )
            ))

        return rooms
