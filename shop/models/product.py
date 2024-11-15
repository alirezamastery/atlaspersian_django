from django.db import models
from django.core.validators import MaxValueValidator
from PIL import Image, UnidentifiedImageError

from utils.slug import unique_slugify


__all__ = [
    'Product',
    'ProductAttributeValue',
]


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, blank=True)
    thumbnail = models.ImageField(upload_to='product/thumbnail')
    score = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5)])

    category = models.ForeignKey(
        'shop.Category',
        on_delete=models.PROTECT,
        related_name='products'
    )
    brand = models.ForeignKey(
        'shop.Brand',
        on_delete=models.PROTECT,
        related_name='products'
    )

    introduction = models.TextField(default='')
    description = models.TextField(default='')

    attribute_values = models.ManyToManyField(
        'shop.Attribute',
        through='shop.ProductAttributeValue',
        # related_name='products', will cause error in queries!
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            slug_str = f'{self.title}'.replace(' ', '-')
            unique_slugify(self, slug_str)

        super().save(*args, **kwargs)

        if self.thumbnail:
            img = Image.open(self.thumbnail.path)
            w = 500
            h = 500
            if img.height > h or img.width > w:
                img.thumbnail((w, h))
                img.save(self.thumbnail.path)


class ProductAttributeValue(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    attribute = models.ForeignKey('shop.Attribute', on_delete=models.CASCADE)

    value = models.TextField()
    extra_info = models.TextField(default='', blank=True)
    # is_active = models.BooleanField(default=True)
    # order = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'attribute'],
                name='unique_product_attribute_value'
            )
        ]
