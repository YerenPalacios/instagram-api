from django.core.validators import RegexValidator ,FileExtensionValidator
from django.contrib.auth import get_user_model as User, authenticate
from django.db.models import Q
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from instagram_app.serializers.message import MessageSerializer, ChatRoomMessageSerializer


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
        model = MessageSerializer.Meta.model
        a= ChatRoomMessageSerializer(
            obj.chatroommessage_set.first()
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