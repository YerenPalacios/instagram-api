import django_filters

from instagram_app.models import Post


class PostFilter(django_filters.FilterSet):
    saved = django_filters.BooleanFilter(field_name='is_saved', label='saved')

    class Meta:
        model = Post
        fields = ['user']
