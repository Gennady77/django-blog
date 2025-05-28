from django.contrib.auth import get_user_model
from rest_framework import serializers
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.core.files.uploadedfile import InMemoryUploadedFile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'avatar', 'birthday', 'gender')

class ProfileAvatarSerializer(serializers.Serializer):
    avatar = serializers.FileField()

    def validate_avatar(self, avatar: 'InMemoryUploadedFile'):
        if avatar.content_type not in ['image/png']:
            raise serializers.ValidationError(code='unsupported image extension')

        return avatar

