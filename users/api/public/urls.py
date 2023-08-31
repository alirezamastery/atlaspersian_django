from django.urls import path
from rest_framework.routers import DefaultRouter

from users.api.public.views import *


app_name = 'users_public'

urlpatterns = [
    path('profile/', ProfileViewPublic.as_view(), name='user-profile-public'),
]

router = DefaultRouter()

router.register('users', UserViewSetPublic)

urlpatterns += router.urls
