from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


app_name = 'shop_api_admin'

router = DefaultRouter()

urlpatterns = [
    path('card-info/', CardInfoView.as_view(), name='card-info'),
]

router.register('categories', CategoryViewSetAdmin, basename='categories')
router.register('products', ProductViewSetAdmin, basename='products')
router.register('brands', BrandViewSetAdmin, basename='brands')
router.register('attributes', AttributeViewSetAdmin, basename='attributes')
router.register('attribute-units', AttributeUnitViewSetAdmin, basename='attribute-units')
router.register('selector-types', VariantSelectorTypeViewSetAdmin, basename='selector_types')
router.register('variants', VariantViewSetAdmin, basename='variants')
router.register('images', ImageViewSetAdmin, basename='images')
router.register('orders', OrderViewSetAdmin, basename='orders')
router.register('questions', QuestionViewSet, basename='questions')
router.register('home-slides', HomeSlideViewSetAdmin, basename='home-slides')
router.register('comments', CommentViewSet, basename='comments')
router.register('payment-methods', PaymentMethodViewSetAdmin, basename='payment-methods')
router.register('shipping-methods', ShippingMethodViewSetAdmin, basename='shipping-methods')

urlpatterns += router.urls
