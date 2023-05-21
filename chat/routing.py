# chat/routing.py
from django.urls import re_path, path
from . import consumers
from .consumers.chat_comsumer import ChatConsumer2, ChatConsumer
from .consumers.video_chat_consumer import VideoChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    path('ws/chat2/', ChatConsumer2.as_asgi()),
    path('ws/video-chat/', VideoChatConsumer.as_asgi()),
]
