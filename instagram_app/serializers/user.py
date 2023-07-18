from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model as User, authenticate
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from instagram_app.models import Follow

from instagram_app.serializers.message import ChatRoomMessageSerializer
from instagram_app.utils import generate_random_color


class UserSerializer(serializers.ModelSerializer):
    is_following = serializers.BooleanField(default=None)

    def get_following(self, obj):
        #TODO: change this weird thing
        return (
            True if self.context.get('request')
            and self.context['request'].user.is_authenticated
            and obj.following.filter(
                follower=self.context['request'].user
            ) else False
        )

    class Meta:
        model = User()
        exclude = ('user_permissions', 'groups', 'is_staff', 'password',)
        read_only_fields = ('name',)


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User()
        fields = ['image', 'name', 'username', 'color']
        read_only_fields = ('name',)


class ChatUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    last_login = serializers.DateTimeField()
    name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField
    image = serializers.CharField
    is_active = serializers.BooleanField()
    description = serializers.CharField()
    color = serializers.CharField()


class ChatMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    content = serializers.CharField()
    is_post = serializers.BooleanField()
    user_id = serializers.IntegerField()
    room_id = serializers.IntegerField()


class ChatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = ChatUserSerializer()
    last_message = ChatMessageSerializer()


class UserChattingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_user(self, obj):
        user =  obj.users.exclude(id = self.context['user'].id)[0]
        return UserSerializer(user).data

    def get_last_message(self, obj):
        a= ChatRoomMessageSerializer(
            obj.chatroommessage_set.last()
        ).data
        return a


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)


class UserSignUpSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User().objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User().objects.all())]
    )

    password = serializers.CharField(max_length=64)

    image = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], 
        required=False
    )
    
    def create(self, validated_data: dict):
        if not validated_data.get('image'):
            validated_data['image'] = None
        password = validated_data.pop('password') 
        user = self.Meta.model.objects.create(**validated_data)
        user.set_password(password)
        user.color = generate_random_color()
        user.save()
        return user

    class Meta:
        model = User()
        fields = '__all__'


class ProfileStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User()
        fields = ['id', 'username', 'image', 'color']


class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    posts_count = serializers.IntegerField(required=False)
    
    def get_followers_count(self, obj):
        return obj.following.count()

    def get_following_count(self, obj):
        return obj.follower.count()

    def get_following(self, obj):
        return True if obj.following.filter(
            follower=self.context['request'].user
        ) else False

    class Meta:
        model = User()
        fields = [
            'id',
            'name',
            'email',
            'image',
            'username',
            'following',
            'description',
            'followers_count',
            'following_count',
            'posts_count',
            'color'
        ]

class UserUpdateSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required=False)
    name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = User()
        fields = [
            'id',
            'name',
            'email',
            'image',
            'username',
            'description'
        ]

class FollowUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['following']

    def create(self, data):
        user = self.context['request'].user
        return Follow.objects.create(
            follower=user,
            following=data['following']
        )


class UserExistsSerializer(serializers.Serializer):
    exists = serializers.BooleanField()
