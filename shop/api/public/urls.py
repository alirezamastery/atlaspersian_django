from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


app_name = 'shop_api_public'

router = DefaultRouter()

urlpatterns = [
    path('home-data/', HomePageDataView.as_view(), name='home-data'),
    path('checkout-opts/', CartCheckoutOptionsView.as_view(), name='cart-checkout-opts'),
    path('verify-discount/', DiscountCodeVerifyView.as_view(), name='verify-discount'),
]

router.register('home-slides', HomeSlideViewSetPublic, basename='home-slides')
router.register('categories', CategoryViewSetPublic, basename='categories')
router.register('brands', BrandViewSetPublic, basename='brands')
router.register('products', ProductViewSetPublic, basename='products')
router.register('orders', OrderViewSetPublic, basename='orders')
router.register('pay-methods', PaymentMethodViewSetPublic, basename='pay-methods')
router.register('shipping-methods', ShippingMethodViewSetPublic, basename='shipping-methods')
router.register('payments', PaymentViewSet, basename='payments')
router.register('comments', CommentViewSetPublic, basename='comments')
router.register('questions', QuestionViewSetPublic, basename='questions')

urlpatterns += router.urls
