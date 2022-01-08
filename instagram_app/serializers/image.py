from rest_framework import serializers

from instagram_app.models import Images

class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ['image']