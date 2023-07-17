from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    GenericAPIView,
    ListCreateAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Count

from instagram_app.models import Follow, User
from instagram_app.serializers import LoginSerializer, UserSerializer, ProfileStoriesSerializer
from instagram_app.serializers.user import FollowUserSerializer, UserDetailSerializer, UserSignUpSerializer, \
    UserExistsSerializer
from instagram_app.services.user_service import UserService


class UserView(ListCreateAPIView):
    serializer_class = UserSerializer
    service = UserService()

    def get_queryset(self):
        limit = self.request.GET.get('page_size')
        return self.service.get_users(
            self.request.GET,
            int(limit) if limit else None,
            self.request.auth.user.id if self.request.auth else None
        )


class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    queryset = serializer_class.Meta.model.objects.annotate(
        posts_count=Count('post'),
    )
    lookup_field = 'username'


class UserSignupView(CreateAPIView):
    serializer_class = UserSignUpSerializer
    service = UserService()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = self.service.create_user(serializer.data)
        auth = self.service.login({'email': user.email, 'password': serializer.data.get("password")})
        return Response(auth, status=201)


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


class UserExistsView(RetrieveAPIView):
    service = UserService()
    serializer_class = UserExistsSerializer

    def get_object(self):
        user_value = self.request.GET.get('value')
        return self.service.get_user_exists(user_value)

