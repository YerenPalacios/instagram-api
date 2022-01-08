from django.urls import path, include
from rest_framework.routers import DefaultRouter
from instagram_app.views.user import UserView, ProfileStoriesView, LoginView, LogoutView
from instagram_app.views.post import PostsView
from instagram_app.views.comment import CommentView
from instagram_app.views.like import LikeView


urlpatterns = [
    path('user/', UserView.as_view()),
    path('post/', PostsView.as_view()),
    path('login/', LoginView.as_view()),  
    path('logout/', LogoutView.as_view()),
    path('like/', LikeView.as_view()),
    path('comment/', CommentView.as_view()),
    path('profile-stories/', ProfileStoriesView.as_view()),
]
