from datetime import datetime
from rest_framework import serializers

from django.contrib.auth import get_user_model as User, authenticate
from django.core.validators import RegexValidator ,FileExtensionValidator
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from instagram_app.models import Comment, Images, Post

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User()
        exclude = ('user_permissions', 'groups','is_staff', 'password',)

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


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User().objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User().objects.all())]
    )
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Debes introducir un número con el siguiente formato: +999999999. El límite son de 15 dígitos."
    )
    phone = serializers.CharField(validators=[phone_regex], required=False)

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    image = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], 
        required=False
    )



class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'

    
class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ['image']
        

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    images = ImagesSerializer(many=True)
    comments = CommentSerializer(many=True)
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return datetime.date(obj.created_at) 

    def get_likes(self, obj):
        return obj.likes.all().count()


    class Meta:
        model = Post
        fields = '__all__'


