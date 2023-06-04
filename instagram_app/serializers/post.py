from rest_framework import serializers

from instagram_app.models import Post
from instagram_app.serializers import ImagesSerializer, UserSerializer, UserPostSerializer
from instagram_app.serializers.comment import CommentSerializer


# TODO: create usernames and retrieve them 
# mod profile, view profile, follow, show following in stories div, auth forms

class PostSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True)
    user = UserPostSerializer()
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    last_owner_comment = serializers.CharField()
    is_liked = serializers.BooleanField(default=None)
    is_saved = serializers.BooleanField(default=None)

    def create(self, validated_data):

        instance = self.Meta.model(**validated_data)

        return instance


    class Meta:
        model = Post
        fields = '__all__'
