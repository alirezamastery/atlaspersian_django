from rest_framework import serializers

from users.models.profile import Profile
from .read import ProfileReadSerializerAdmin


__all__ = [
    'ProfileWriteSerializerAdmin',
]


class ProfileWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'avatar',
            'social_id',
            'birth_date',
        ]

    def to_representation(self, instance):
        return ProfileReadSerializerAdmin(instance, context=self.context).data
