from rest_framework import serializers

from users.models import Profile


class _ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'avatar',
            'social_id',
            'birth_date',
        ]


class _ProfilePublicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'avatar',
        ]
