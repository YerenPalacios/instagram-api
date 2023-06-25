from rest_framework import serializers

from instagram_app.models import Files

class FilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Files
        fields = ['file']
