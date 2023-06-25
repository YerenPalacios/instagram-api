from rest_framework import serializers

from instagram_app.models import Files

class FilesSerializer(serializers.ModelSerializer):
    thumbnail = serializers.CharField(required=False)

    class Meta:
        model = Files
        fields = ['file', 'thumbnail']
