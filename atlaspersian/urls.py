from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),

    path('api/admin/auth/', include('users.api.admin.urls')),
    path('api/admin/shop/', include('shop.api.admin.urls')),

    path('api/public/auth/', include('users.api.public.urls')),
    path('api/public/shop/', include('shop.api.public.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
