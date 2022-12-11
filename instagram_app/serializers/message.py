from rest_framework import serializers

from instagram_app.models import Message
from chat.models import ChatRoomMessage


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class ChatRoomMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRoomMessage
        fields = '__all__'
