from asgiref.sync import async_to_sync
from channels.exceptions import DenyConnection
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer

from chat.services.chat_service import ChatService
from instagram_app.services.user_service import UserService


class VideoChatConsumer(WebsocketConsumer):

    available_actions = ['get_messages', 'add_message']
    chat_room = None
    service = ChatService()
    user_service = UserService()

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_id = None

    def get_query_data(self):
        params = self.scope['query_string'].decode('utf-8').split('&')

        token_key, token_value = params[1].replace("'", "").split('=')
        if token_key != 'token':
            raise DenyConnection('tampoco sirve')

        room_key, room_id = params[0].replace("'", "").split('=')
        if room_key != 'room_id':
            raise DenyConnection('tampoco sirve el room id')

        return {"room_id": room_id, "token": token_value}

    def set_room(self):
        try:
            data = self.get_query_data()
            self.scope['user'] = self.user_service.get_current_user(data['token'])
            self.chat_id = data['room_id']
        except DenyConnection as e:
            self.send_json({'detail': str(e)})
            raise DenyConnection(e)

    def connect(self):
        self.accept()
        self.set_room()

        # Join chat
        async_to_sync(self.channel_layer.group_add)(
            self.chat_id,
            self.channel_name
        )
        print('VIDEO connected')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_id,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data: bytes = None):
        async_to_sync(self.channel_layer.group_send)(
            self.chat_id, {"type": "send_video", "bytes": bytes_data}
        )

    def send_video(self, data):
        import io
        print(io.BytesIO(data['bytes']))
        self.send(bytes_data=data['bytes'])

    def receive_json(self, data, **kwargs):
        action = data.get('action')

        if not action:
            return self.send_json({'detail': 'No action provided'})

        if data['action'] in self.available_actions:
            async_to_sync(self.channel_layer.group_send)(
                self.chat_id, {"type": data['action'], "bytes": data['text']}
            )
