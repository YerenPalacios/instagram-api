import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from chat.models import ChatRoom
from chat.services.chat_service import ChatService
from instagram_app.services.user_service import UserService


logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
)


class ChatConsumer2(JsonWebsocketConsumer):

    available_actions = ['get_messages', 'add_message']
    chat_room = None
    service = ChatService()
    user_service = UserService()

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_id = None

    def get_query_data(self):
        params = self.scope['query_string'].decode('utf-8').split('&')
        if len(params) != 2:
            raise ValueError('no sirve')

        token_key, token_value = params[1].replace("'", "").split('=')
        if token_key != 'token':
            raise ValueError('tampoco sirve')

        room_key, room_id = params[0].replace("'", "").split('=')
        if room_key != 'room_id':
            raise ValueError('tampoco sirve el room id')

        return {"room_id": room_id, "token": token_value}

    def set_room(self):
        try:
            data = self.get_query_data()
            self.scope['user'] = self.user_service.get_current_user(data['token'])
            self.chat_id = data['room_id']
        except ValueError as e:
            self.send_json({'detail': str(e)})
            self.close()

    def connect(self):
        self.accept()
        self.set_room()

        # Join chat
        async_to_sync(self.channel_layer.group_add)(
            self.chat_id,
            self.channel_name
        )
        self.get_messages()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_id,
            self.channel_name
        )

    def receive_json(self, data, **kwargs):
        action = data.get('action')

        if not action:
            return self.send_json({'detail': 'No action provided'})

        if data['action'] in self.available_actions:
            async_to_sync(self.channel_layer.group_send)(
                self.chat_id, {"type": data['action'], "text": data['text']}
            )

    def add_message(self, data):
        """ Create a chat message """
        message = self.service.create_message(
            self.scope['user'].id,
            self.get_query_data()['room_id'],
            data['text']
        )
        self.send_json(message)

    def get_messages(self):
        """ return list of messages by room """
        #TODO: review this calls
        room_id = self.get_query_data()['room_id']
        room = ChatRoom.objects.get(id=room_id)
        self.scope['room'] = room
        messages = self.service.get_messages_by_room(int(room_id))
        self.send_json({'type': 'get_messages', 'data': messages})