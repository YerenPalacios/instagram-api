from django.db.models import Prefetch
from rest_framework.authtoken.models import Token
from rest_framework.generics import  ListAPIView, GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from instagram_app.models import Images, User, Comment, Like
from instagram_app.serializers import LoginSerializer, PostSerializer, UserSerializer, CommentSerializer, CommentViewSerializer, LikeSerializer, ProfileStoriesSerializer

# Create your views here.

class UserView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()

class PostsView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = self.serializer_class.Meta.model.objects.prefetch_related(
            Prefetch('likes', queryset=Like.objects.filter(user=self.request.user)), 
            Prefetch(
                'comments',
                queryset=Comment.objects.filter(
                    user=self.request.user
                ).select_related('user')
            ),
            'images'
        )
        return queryset

    def get_serializer_context(self):
        context = super(PostsView, self).get_serializer_context()
        context.update({'user' : self.request.user})
        return context

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


class CommentView(ListCreateAPIView):
    serializer_class = CommentViewSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def list(self, request):
        query = self.queryset.filter(user = request.user)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data)

    def create(self, request):
        print(request.data)
        data = {
            'post':request.data.get('post'),
            'text':request.data.get('text'),
            'user':request.user.id
        }
        serializer = self.serializer_class(data=data, context=data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response({
            'comments':CommentSerializer(
                comment.post.comments.all(), many=True
            ).data
        })


class LikeView(ListCreateAPIView):
    serializer_class = LikeSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def create(self, request):
        print(request.data)
        data = {
            'post':request.data.get('post'),
            'user':request.user.id
        }
        serializer = self.serializer_class(data=data, context=data)
        serializer.is_valid(raise_exception=True)
        if serializer.save():
            return Response({'liked':True})
        return Response({'liked':False})


class ProfileStoriesView(ListAPIView):
    serializer_class = ProfileStoriesSerializer
    queryset = User.objects.all()
        
        
