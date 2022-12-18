from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model as User, authenticate
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from instagram_app.models import Follow

from instagram_app.serializers.message import ChatRoomMessageSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User()
        exclude = ('user_permissions', 'groups','is_staff', 'password',)
        read_only_fields = ('name',)


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

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User()
        fields = ('username', 'email')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)

    def validate(self, data):
        user = authenticate(email=data['email'],password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid username or password')

        self.context['user'] = user
        return data
    
    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


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
    
    def create(self, validated_data:dict):
        if not validated_data.get('image'):
            validated_data['image'] = None
        password = validated_data.pop('password') 
        user = self.Meta.model.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User()
        fields = '__all__'


class ProfileStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User()
        fields = ['id','username','image']


class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    
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
            'following_count'
        ]


class FollowUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['following']

    def create(self, data):
        user = self.context['request'].user
        return Follow.objects.create(
            follower = user,
            following = data['following']
        )