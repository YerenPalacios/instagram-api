from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from instagram_app.models import PublicChatRoom, PublicChatRoomMessage

from instagram_app.models import Comment, Follow, Like, Message, Post, User, Files

# Register your models here.

models = [Like, Comment, Follow, Files, Message]

admin.site.register(models)

@admin.register(PublicChatRoom)
class PublicChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['id', 'title']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['name']


class CachingPaginator(Paginator):
    def _get_count(self):
        if not hasattr(self, '_count'):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)
            except:
                self._count = len(self.object_list)
        
        return self._count

    count = property(_get_count)

@admin.register(PublicChatRoomMessage)
class PublicChatRoomMessageAdmin(admin.ModelAdmin):
    list_filter = ['room','user', 'timestamp']
    list_display = ['room','user', 'timestamp', 'content']
    search_fields = ['room__title','user__username', 'content']
    readonly_fields = ['id', 'room','user', 'timestamp']

    show_full_result_count = False
    paginator = CachingPaginator
