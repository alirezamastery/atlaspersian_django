from rest_framework import serializers

from shop.models import *


class ProductScoreSerializerPublic(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    score = serializers.IntegerField(min_value=1, max_value=5)

    def validate(self, attrs):
        request = self.context.get('user')
        product = attrs['product']
        order_ids = Order.objects.filter(user=request.user).values_list('id', flat=True)
        if not OrderItem.objects.filter(id__in=order_ids, item__product=product).exists():
            raise serializers.ValidationError('you have not purchased this product')

        return attrs
