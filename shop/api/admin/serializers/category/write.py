from rest_framework import serializers

from shop.models import *
from .read.main import ProductCategoryDetailSerializer


__all__ = [
    'ProductCategoryWriteSerializer',
]


class ProductCategoryWriteSerializer(serializers.Serializer):
    title = serializers.CharField()
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    selector_type = serializers.PrimaryKeyRelatedField(queryset=SelectorType.objects.all())
    attributes = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all()),
        allow_empty=True,
        default=[]
    )
    brands = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all()),
        allow_empty=True,
        default=[]
    )

    class Meta:
        fields = ['title', 'parent', 'selector_type', 'attributes']

    def create(self, validated_data):
        attr_ids = set(attr.id for attr in validated_data.pop('attributes'))
        brand_ids = set(brand.id for brand in validated_data.pop('brands'))

        parent_node = validated_data['parent']
        child_data = {
            'title':         validated_data['title'],
            'selector_type': validated_data['selector_type']
        }
        if parent_node is None:
            category = Category.add_root(**child_data)
        else:
            category = parent_node.add_child(**child_data)

        for attr_id in attr_ids:
            CategoryAttribute.objects.create(category=category, attribute_id=attr_id)

        for brand_id in brand_ids:
            CategoryBrand.objects.create(category=category, brand_id=brand_id)

        return category

    def update(self, category, validated_data):
        category.title = validated_data.get('title', category.title)
        category.save()

        parent_node = validated_data.get('parent', -1)
        if parent_node != -1:
            if parent_node is None:
                category.move(Category.get_first_root_node(), pos='sorted-sibling')
            elif not parent_node.id == category.id:
                category.move(parent_node, pos='sorted-child')

        self.handle_attributes(category, validated_data)
        self.handle_brands(category, validated_data)

        return category

    @staticmethod
    def handle_attributes(category, validated_data):
        current_attrs = CategoryAttribute.objects.filter(category=category)
        current_attr_ids = set(attr.attribute_id for attr in current_attrs)
        request_attr_ids = set(attr.id for attr in validated_data.get('attributes', []))
        new_attr_ids = request_attr_ids - current_attr_ids
        removed_attr_ids = current_attr_ids - request_attr_ids

        for new_attr_id in new_attr_ids:
            CategoryAttribute.objects.create(category=category, attribute_id=new_attr_id)

            product_attr_objs = []
            for product in category.products.all():
                product_attr_objs.append(
                    ProductAttributeValue(product=product, attribute_id=new_attr_id, value='')
                )
            ProductAttributeValue.objects.bulk_create(product_attr_objs)

        for removed_attr_id in removed_attr_ids:
            try:
                CategoryAttribute.objects.get(category=category, attribute_id=removed_attr_id).delete()
            except CategoryAttribute.DoesNotExist:
                pass
            for product in category.products.all():
                try:
                    ProductAttributeValue.objects.get(attribute_id=removed_attr_id, product=product).delete()
                except ProductAttributeValue.DoesNotExist:
                    pass

    @staticmethod
    def handle_brands(category, validated_data):
        current_brands = CategoryBrand.objects.filter(category=category)
        current_brand_ids = set(cat_brands.brand_id for cat_brands in current_brands)
        request_brand_ids = set(brand.id for brand in validated_data.get('brands', []))
        new_brand_ids = request_brand_ids - current_brand_ids
        removed_brand_ids = current_brand_ids - request_brand_ids

        for new_brand_id in new_brand_ids:
            CategoryBrand.objects.create(category=category, brand_id=new_brand_id)

        for removed_brand_id in removed_brand_ids:
            try:
                CategoryBrand.objects.get(category=category, brand_id=removed_brand_id).delete()
            except CategoryBrand.DoesNotExist:
                pass

    def save(self, **kwargs):
        instance = super().save(**kwargs)

        self.instance = (Category.objects
                         .prefetch_related('attributes__unit')
                         .prefetch_related('brands')
                         .get(id=instance.id))
        return self.instance

    def to_representation(self, category):
        return ProductCategoryDetailSerializer(category).data
