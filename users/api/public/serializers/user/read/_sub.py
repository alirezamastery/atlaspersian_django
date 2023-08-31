from rest_framework import serializers

from users.models import Profile


class _ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'avatar',
            'created_at',
            'updated_at',
        ]
