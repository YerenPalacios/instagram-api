from django.contrib import admin

from instagram_app.models import Comment, Follow, Like, Post, User, Images

# Register your models here.

models = [Post, User, Like, Comment, Follow, Images]

admin.site.register(models)
