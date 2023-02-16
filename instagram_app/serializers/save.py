from rest_framework import serializers

from instagram_app.models import Save


class SaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Save
        fields = '__all__'

    def save(self, **kwargs):
        saves = self.Meta.model.objects.filter(
            user=self.context['user'], post=self.context['post']
        )
        if saves.count() > 0:
            saves.delete()
            return False
        return super().save()
