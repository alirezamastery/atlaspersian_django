from shop.models import *


__all__ = [
    'get_variant_final_price',
]


def get_variant_final_price(variant: Variant) -> int:
    if variant.discount > 0:
        final_price = (variant.price * (100 - variant.discount)) // 100
        return int(final_price / 10000) * 10000
    return variant.price
