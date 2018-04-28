from django.conf.urls import url, include
from django.contrib import admin

# For development
from django.conf import settings
from django.conf.urls.static import static
# For development

urlpatterns = [
    url(r'^', include('shop.urls', namespace='shop')),
    url(r'^users/', include('profiles.urls', namespace='users')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
