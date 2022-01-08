from rest_framework import serializers

from instagram_app.models import Post
from instagram_app.serializers import ImagesSerializer, UserSerializer
from instagram_app.serializers.comment import CommentSerializer


# TODO: create usernames and retrieve them 
# mod profile, view profile, follow, show following in stories div, auth forms

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    images = ImagesSerializer(many=True)
    comments = serializers.SerializerMethodField()
    user = UserSerializer()
    count_comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_comments(self, obj):
        data = obj.comments.all()
        return CommentSerializer(data, many=True).data

    def get_is_liked(self, obj):
        if len(obj.likes.all()) == 1:
            return True
        return False

    def get_count_comments(self, obj): 
        return obj.comments.all().count()

    def get_likes(self, obj):
        return obj.likes.all().count()


    class Meta:
        model = Post
        fields = '__all__'
