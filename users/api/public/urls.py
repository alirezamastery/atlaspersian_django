from django.urls import path
from rest_framework.routers import DefaultRouter

from users.api.public.views import *


app_name = 'users_public'

urlpatterns = [
    path('csrf/', CSRFView.as_view(), name='csrf-public'),
    path('exist/', UserExistView.as_view(), name='user-exist'),
    path('login/', LoginView.as_view(), name='login-public'),
    path('logout/', LogoutView.as_view(), name='logout-public'),
    path('profile/', ProfileViewPublic.as_view(), name='user-profile-public'),
]

router = DefaultRouter()

router.register('users', UserViewSetPublic)

urlpatterns += router.urls
