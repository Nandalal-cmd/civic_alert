from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from complaints.views import admin_dashboard

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', admin_dashboard, name='admin_dashboard_root'),
    path('', include('complaints.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)