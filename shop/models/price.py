# from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
#
#
# __all__ = [
#     'PriceModel',
# ]
#
#
# class PriceModel(models.Model):
#     discount_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(99)])
#     raw_price = models.PositiveBigIntegerField(validators=[MinValueValidator(10000)])
#     discounted_price = models.PositiveBigIntegerField(validators=[MinValueValidator(10000)])
#     selling_price = models.PositiveBigIntegerField(validators=[MinValueValidator(10000)])
#
#     class Meta:
#         abstract = True
