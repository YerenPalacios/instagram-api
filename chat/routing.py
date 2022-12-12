# chat/routing.py
from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/chat2/', consumers.ChatConsumer2.as_asgi()),
]