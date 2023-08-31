from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


app_name = 'shop_api_public'

router = DefaultRouter()

urlpatterns = [
]

router.register('categories', CategoryViewSetPublic, basename='categories')
router.register('brands', BrandViewSetPublic, basename='brands')
router.register('products', ProductViewSetPublic, basename='products')
router.register('orders', OrderViewSetPublic, basename='orders')

urlpatterns += router.urls
