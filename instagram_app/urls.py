from django.urls import path, include
from rest_framework.routers import DefaultRouter
from instagram_app.views import (
    PostsView, UserView, LoginView, LogoutView, LikeView, CommentView, ProfileStoriesView)


urlpatterns = [
    path('user/', UserView.as_view()),
    path('post/', PostsView.as_view()),
    path('login/', LoginView.as_view()),  
    path('logout/', LogoutView.as_view()),
    path('like/', LikeView.as_view()),
    path('comment/', CommentView.as_view()),
    path('profile-stories/', ProfileStoriesView.as_view()),
]
