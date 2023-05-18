from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    GenericAPIView,
    ListCreateAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Count

from instagram_app.models import Follow, User
from instagram_app.serializers import LoginSerializer, UserSerializer, ProfileStoriesSerializer
from instagram_app.serializers.user import FollowUserSerializer, UserDetailSerializer, UserSignUpSerializer
from instagram_app.services.user_service import UserService


class UserView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()


class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    queryset = serializer_class.Meta.model.objects.annotate(
        posts_count=Count('post'),
    )
    lookup_field = 'username'


class UserSignupView(CreateAPIView):
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = serializer.create(serializer.data)
        token = Token.objects.create(user=user)
        data = {
            'user': UserSerializer(user).data,
            'token': token.key
        }
        return Response(data, status=201)


class LoginView(GenericAPIView):
    name = "login"
    serializer_class = LoginSerializer
    queryset = User.objects.filter(is_active=True)

    def __init__(self):
        super().__init__()
        self.service = UserService()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.service.login(serializer.data)
        return Response(data, status=201)


class LogoutView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = Token.objects.get(user=request.user)
        if token:
            token.delete()
            return Response(status=204)
        else:
            return Response({'message': 'user not found'}, status=400)


class ProfileStoriesView(ListAPIView):
    name = "profile-stories"
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileStoriesSerializer

    def __init__(self):
        super().__init__()
        self.service = UserService()

    def get_queryset(self):
        return self.service.get_following_users(self.request.user.id)


class FollowUserView(CreateAPIView, DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowUserSerializer
    queryset = Follow.objects.all()

    def delete(self, request, *args, **kwargs):
        obj = Follow.objects.get(
            follower=request.auth.user, following_id=request.data['following'])
        obj.delete()
        return Response({}, 200)
