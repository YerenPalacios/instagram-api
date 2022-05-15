# chat/consumers.py
import json
import logging

from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from channels.consumer import SyncConsumer

from instagram_app.serializers.message import MessageSerializer, ChatRoomMessageSerializer
from chat.models import *

logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


def get_messages(user, send_to):
    # qs = MessageSerializer.Meta.model.objects.filter(
    #         Q(user=user) & Q(send_to=send_to) |
    #         Q(user=send_to) & Q(send_to=user)
    #     ).order_by('created_at')
    return qs

def save_message(msg, by_user):
    model = MessageSerializer.Meta.model
    a = model.objects.create(
        text=msg['text'],
        user_id=by_user.id,
        send_to_id=msg['send_to']
    )
    message = MessageSerializer(a).data
    return message

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

class ChatConsumer2(JsonWebsocketConsumer):

    available_actions = ['get_messages', 'add_message']
    chat_room = None

    def update_headers(self):
        b_headers = dict(self.scope['headers'])
        self.scope['headers'] = {k.decode('utf-8'): b_headers.get(k).decode('utf-8') for k in b_headers}

    def set_user(self):
        auth = self.scope['cookies'].get('Authorization')
        if auth:
            try:
                token_name, token_key = auth.split()
                if token_name == 'Token':
                    token = Token.objects.get(key=token_key)
                    self.scope['user'] = token.user
            except Token.DoesNotExist:
                raise
        else:
            raise

    def connect(self):
        self.update_headers()
        self.set_user()

        self.chat_id = self.scope['cookies'].get('chat-id')

        # Join chat
        async_to_sync(self.channel_layer.group_add)(
            self.chat_id,
            self.channel_name
        )

        self.accept()
        self.get_messages()

    # def receive(self, event):
    #     data = json.loads(event['text'])
        

    #     if data['action'] == 'get_messages':
    #         initial_messages = get_messages(self.scope['user'], data['send_to'])

    #         self.send({
    #             "type": "websocket.send",
    #             "text": json.dumps(MessageSerializer(initial_messages, many=True).data),
    #         })
    #     elif data['action'] == 'add_message':
    #         saved_message = save_message(data['text'], self.scope['user'])
    #         self.send({
    #             "type": "websocket.send",
    #             "text": json.dumps(saved_message),
    #         })
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive_json(self, data):
        action = data.get('action')

        if not action:
            return self.send_json({'error':'No action provided'})

        if data['action'] in self.available_actions:
            # saved_message = save_message(data['text'], self.scope['user'])
            if data['action'] == 'add_message':
                message = ChatRoomMessage.objects.create(
                    user=self.scope['user'], 
                    room=self.scope['room'],
                    content=data['text']
                )
                async_to_sync(self.channel_layer.group_send)(
                    self.chat_id,
                    {
                        "type": data['action'],
                        "text": ChatRoomMessageSerializer(message).data,
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.chat_id,
                    {
                        "type": data['action'],
                        "text": data['text'],
                    }
                )

        # Send message to room group
        

    # Receive message from room group
    def add_message(self, data):
   
        self.send_json(data)

    def get_messages(self):
        room = ChatRoom.objects.get(id=self.scope['cookies'].get('chat-id'))
        self.scope['room'] = room
        messages = ChatRoomMessageSerializer(room.chatroommessage_set.all(), many=True).data
        self.send_json({'type':'get_messages','data':messages})