# chat/routing.py
from django.urls import path

from chat.consumers.chat_consumer import ChatConsumer2

websocket_urlpatterns = [
    path('ws/chat2/', ChatConsumer2.as_asgi()),
]
