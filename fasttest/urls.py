from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from fasttest import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls')),
    path('attachments/', include('attachments.urls', namespace='attachments')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
