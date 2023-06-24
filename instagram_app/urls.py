from django.urls import path

from instagram_app.views.message import MessageView, ChatListView
from instagram_app.views.user import (
    FollowUserView, UserDetailView, UserView, ProfileStoriesView, LoginView, LogoutView, UserSignupView
)
from instagram_app.views.post import PostsView, PostDetailView, SharePostView
from instagram_app.views.comment import CommentView
from instagram_app.views.like import LikeView
from instagram_app.views.save import SaveView


urlpatterns = [
    path('user/', UserView.as_view()),
    path('user/<str:username>', UserDetailView.as_view()),
    path('sign-up/', UserSignupView.as_view()),
    path('login/', LoginView.as_view(), name=LoginView.name),
    path('logout/', LogoutView.as_view()),
    path('profile-stories/', ProfileStoriesView.as_view(), name=ProfileStoriesView.name),
    path('follow/', FollowUserView.as_view()),

    path('post/', PostsView.as_view(), name=PostsView.name),
    path('post/<int:pk>', PostDetailView.as_view()),

    path('like/', LikeView.as_view()),
    path('save/', SaveView.as_view()),

    path('comment/', CommentView.as_view()),

    path('message/', MessageView.as_view()),
    path('chatlist/', ChatListView.as_view()),
    path(SharePostView.path, SharePostView.as_view())
]
