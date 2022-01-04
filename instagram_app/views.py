from django.db.models import query
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import  CreateAPIView, GenericAPIView, ListCreateAPIView
from instagram_app.models import Images, User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from instagram_app.serializers import LoginSerializer, PostSerializer, UserSerializer, CommentSerializer

# Create your views here.

class UserView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()

class PostsView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = serializer_class.Meta.model.objects.prefetch_related('likes', 'comments', 'images')

    def create(self, request):
        model = self.serializer_class.Meta.model
        post = model.objects.create(
            user=self.request.user,
            text=self.request.data['text']
        )
        images = request.data.get('images', [])
        if len(images) > 0:
            for image in images:
                Images.objects.create(image=image, user=self.request.user)

        post = self.serializer_class(post).data

        return Response(post, status=201)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.filter(is_active=True)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': self.serializer_class(user).data,
            'token': token
        }
        return Response(data,status=201)

class LogoutView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = Token.objects.get(user=request.user)
        if token:
            token.delete()
            return Response(status=204)
        else:
            return Response({'message':'user not found'}, status=400)


class Comment(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = serializer_class.Meta.model.objects.all()
