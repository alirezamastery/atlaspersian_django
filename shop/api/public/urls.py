from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


app_name = 'shop_api_public'

router = DefaultRouter()

urlpatterns = [
    path('checkout-opts/', CartCheckoutOptionsView.as_view(), name='cart-checkout-opts')
]

router.register('categories', CategoryViewSetPublic, basename='categories')
router.register('brands', BrandViewSetPublic, basename='brands')
router.register('products', ProductViewSetPublic, basename='products')
router.register('orders', OrderViewSetPublic, basename='orders')
router.register('pay-methods', PaymentMethodViewSetPublic, basename='pay-methods')
router.register('shipping-methods', ShippingMethodViewSetPublic, basename='shipping-methods')
router.register('questions', QuestionViewSetPublic, basename='questions')

urlpatterns += router.urls
