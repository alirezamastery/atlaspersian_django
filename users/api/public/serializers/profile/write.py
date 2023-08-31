from rest_framework import serializers

from users.models.profile import Profile
from .read import ProfileReadSerializerPublic


__all__ = [
    'ProfileWriteSerializerPublic',
]


class ProfileWriteSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar', 'gender']

    def to_representation(self, instance):
        return ProfileReadSerializerPublic(instance, context=self.context).data
