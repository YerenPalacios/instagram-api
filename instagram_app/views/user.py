from rest_framework.response import Response
from rest_framework.generics import  ListAPIView, GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from instagram_app.models import User
from instagram_app.serializers import LoginSerializer, UserSerializer, ProfileStoriesSerializer


class UserView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()


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


class ProfileStoriesView(ListAPIView):
    serializer_class = ProfileStoriesSerializer
    queryset = User.objects.all()
