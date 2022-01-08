from rest_framework import serializers

from instagram_app.models import Comment
from instagram_app.serializers import UserSerializer


class CommentViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
