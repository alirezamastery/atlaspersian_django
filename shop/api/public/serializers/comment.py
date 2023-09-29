from rest_framework import serializers

from shop.models import *


__all__ = [
    'CommentWriteSerializerPublic',
]


class CommentWriteSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'product',
            'text',
            'quality_score',
            'worth_buy_score',
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        product = attrs['product']
        # order_ids = Order.objects.filter(user=request.user).values_list('id', flat=True)
        # print(f'{order_ids = }')
        # if not OrderItem.objects.filter(order_id__in=order_ids, item__product=product).exists():
        #     raise serializers.ValidationError('you have not purchased this product')

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(user=request.user, **validated_data)
        return comment
