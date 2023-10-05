import json
import os
from pathlib import Path
import random

from django.core.management import BaseCommand
from django.db.models import *
from django.db.models.functions import *

from shop.models import *


COLORS = {
    1:  {'hex': '#212121', 'name': 'مشکی', 'bg_hex': '#FFFFFF'},
    2:  {'hex': '#FFFFFF', 'name': 'سفید'},
    3:  {'hex': '#f44336', 'name': 'قرمز'},
    4:  {'hex': '#2196f3', 'name': 'آبی'},
    5:  {'hex': '#ffeb3b', 'name': 'زرد'},
    6:  {'hex': '#00e676', 'name': 'سبز'},
    7:  {'hex': '#FF80AB', 'name': 'صورتی'},
    8:  {'hex': '#9C27B1', 'name': 'بنفش'},
    9:  {'hex': '#002171', 'name': 'سرمه ای'},
    11: {'hex': '#9E9E9E', 'name': 'خاکستری'},
    12: {'hex': '#dedede', 'name': 'نقره ای'},
    14: {'hex': '#562e1f', 'name': 'قهوه ای'},
    15: {'hex': '#c99212', 'name': 'طلایی'},
    17: {'hex': '#ff5722', 'name': 'نارنجی'},
    32: {'hex': '#C71585', 'name': 'چند رنگ'},
    35: {'hex': '#FFFFFE', 'name': 'بی رنگ'},
    39: {'hex': '#e0e0e0', 'name': 'طوسی'},
    85: {'hex': '#ffc001', 'name': 'عسلی'},
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        SelectorType.objects.create(title='رنگ', code='COLOR')
        SelectorType.objects.create(title='سایز', code='SIZE')

        with open('./dump/selectors.json', 'r', encoding='utf-8') as f:
            selectors = json.load(f)
            for s in selectors:
                val = s['extra_info']
                if s['selector_type']['title'] == 'size':
                    val = s['value']
                SelectorValue.objects.create(
                    id=s['id'],
                    type_id=s['selector_type']['id'],
                    title=s['value'],
                    value=val
                )

        with open('./dump/brands.json', 'r', encoding='utf-8') as f:
            brands = json.load(f)
            for brand in brands:
                Brand.objects.create(
                    id=brand['id'],
                    title=brand['title']
                )

        attr_unit_litr = AttributeUnit.objects.create(title='لیتر')
        attr_unit_kilo = AttributeUnit.objects.create(title='کلیو')

        attr_has_lock = Attribute.objects.create(
            title='قفل',
            type=Attribute.Types.BOOLEAN,
        )
        attr_floors_num = Attribute.objects.create(
            title='تعداد طبقه',
            type=Attribute.Types.NUMBER,
        )
        attr_inner_volume = Attribute.objects.create(
            title='حجم داخلی',
            type=Attribute.Types.NUMBER,
            unit=attr_unit_litr,
        )
        attr_weight = Attribute.objects.create(
            title='وزن',
            type=Attribute.Types.NUMBER,
            unit=attr_unit_kilo,
        )
        attr_material = Attribute.objects.create(
            title='جنس',
            type=Attribute.Types.SHORT_TEXT,
        )

        with open('./dump/product_types.json', 'r', encoding='utf-8') as f:
            product_types = json.load(f)
            for i, product_type in enumerate(product_types, start=1):
                print(f'{product_type = }')
                category = Category.objects.create(
                    id=product_type['id'],
                    title=product_type['title'],
                    selector_type_id=product_type['selector_type']['id'],
                    depth=1,
                    path=f'{i:0>4}'
                )
                CategoryAttribute.objects.create(attribute=attr_has_lock, category=category)
                CategoryAttribute.objects.create(attribute=attr_floors_num, category=category)
                CategoryAttribute.objects.create(attribute=attr_inner_volume, category=category)
                CategoryAttribute.objects.create(attribute=attr_weight, category=category)
                CategoryAttribute.objects.create(attribute=attr_material, category=category)

        # Products:
        path = 'media/shop/products/thumbnail'
        images = []
        for dirpath, dirname, filenames in os.walk(path):
            images.extend([f'{path.replace("media/", "")}/{f}' for f in filenames])
            break

        brand_ids = Brand.objects.all().values_list('id', flat=True)
        category_ids = Category.objects.all().values_list('id', flat=True)

        with open('./dump/products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)

        for p in products:
            img = images.pop()
            category = Category.objects.get(id=random.choice(category_ids))
            product = Product.objects.create(
                id=p['id'],
                brand_id=random.choice(brand_ids),
                title=p['title'],
                description='تست میکنیم',
                thumbnail=img,
                category=category,
            )
            ProductImage.objects.create(product=product, is_main=True, file=img)
            print(product)

            ProductAttributeValue.objects.create(attribute=attr_has_lock, product=product, value='دارد')
            ProductAttributeValue.objects.create(attribute=attr_floors_num, product=product, value='3')
            ProductAttributeValue.objects.create(attribute=attr_inner_volume, product=product, value='120')
            ProductAttributeValue.objects.create(attribute=attr_weight, product=product, value='4')
            ProductAttributeValue.objects.create(attribute=attr_material, product=product, value='پلاستیک')

        # Variants:
        with open('./dump/variants.json', 'r', encoding='utf-8') as f:
            variants = json.load(f)
        for v in variants:
            variant = Variant.objects.create(
                product_id=v['product']['id'],
                selector_value_id=v['selector']['id'],
                raw_price=random.randrange(1000, 100_000) * 1000,
                inventory=random.randrange(0, 5),
                max_in_order=5
            )
            print(variant)
