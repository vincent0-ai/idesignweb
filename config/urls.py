"""
Root URL configuration for idesignweb.
Routes public marketing zone, member portal zone, and Django admin.
"""

from django.contrib import admin
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.portal.urls')),
    path('', include('apps.public.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
