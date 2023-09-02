from rest_framework import serializers

from users.models.profile import Profile


__all__ = [
    'ProfileReadSerializerAdmin',
]


class ProfileReadSerializerAdmin(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(method_name='get_avatar_full_url')

    class Meta:
        model = Profile
        fields = '__all__'

    def get_avatar_full_url(self, obj):
        if not obj.avatar:
            return None
        avatar_url = obj.avatar.url
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(avatar_url)
        if (host := self.context.get('host')) is not None:
            return f'{host}{avatar_url}'
        return avatar_url
