from rest_framework import serializers

from instagram_app.models import Like

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

    def save(self, **kwargs):
        likes = self.Meta.model.objects.filter(user = self.context['user'], post = self.context['post'])
        if len(likes)>0:
            for like in likes:
                like.delete()
            return False
        return super().save()