import django_filters

from instagram_app.models import Post


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['user']
