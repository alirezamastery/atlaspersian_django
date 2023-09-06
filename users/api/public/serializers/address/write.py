from rest_framework import serializers

from users.models import Address
from .read import AddressReadSerializerPublic


__all__ = [
    'AddressWriteSerializerPublic',
]


class AddressWriteSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'title',
            'postal_code',
            'province',
            'city',
            'details',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        address = Address.objects.create(user=request.user, **validated_data)
        return address

    def save(self, **kwargs):
        address = super().save(**kwargs)
        address = Address.objects.select_related('province', 'city').get(pk=address.pk)
        return address

    def to_representation(self, instance):
        return AddressReadSerializerPublic(instance).data
