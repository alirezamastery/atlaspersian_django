from django.urls import path
from rest_framework.routers import DefaultRouter

from users.api.public.views import *


app_name = 'users_public'

urlpatterns = [
    path('csrf/', CSRFView.as_view(), name='csrf-public'),
    # path('check-mobile/', CheckMobileView.as_view(), name='check-mobile'),

    path('send-auth-otp/', SendAuthenticationOtpView.as_view(), name='send-auth-otp'),
    path('verify-auth-otp/', VerifyAuthenticationOtpView.as_view(), name='verify-auth-otp'),

    path('login/', LoginView.as_view(), name='login-public'),
    path('logout/', LogoutView.as_view(), name='logout-public'),

    path('forgot-password-otp/', ForgotPasswordSendOtpView.as_view(), name='forgot-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('user-addresses/', UserAddressListView.as_view(), name='user-addresses'),
    # path('profile/', ProfileViewPublic.as_view(), name='user-profile-public'),
]

router = DefaultRouter()

router.register('addresses', AddressViewSetPublic, basename='addresses')
router.register('provinces', ProvinceViewSetPublic, basename='provinces')
router.register('cities', CityViewSetPublic, basename='cities')

urlpatterns += router.urls
