from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import HomeSlide


__all__ = [
    'HomeSlideReadSerializerAdmin',
    'HomeSlideWriteSerializerAdmin',
]


class HomeSlideReadSerializerAdmin(ModelSerializer):
    image = serializers.SerializerMethodField(method_name='get_absolute_url')

    class Meta:
        model = HomeSlide
        fields = [
            'id',
            'image',
            'link',
            'alt',
            'description',
        ]

    def get_absolute_url(self, obj):
        if not obj.image:
            return None
        url = obj.image.url
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(url)
        if (host := self.context.get('host')) is not None:
            return f'{host}{url}'
        return url


class HomeSlideWriteSerializerAdmin(ModelSerializer):
    image = serializers.CharField()

    class Meta:
        model = HomeSlide
        fields = [
            'image',
            'link',
            'alt',
            'description',
        ]


