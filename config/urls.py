"""
Root URL configuration for idesignweb.
Routes public marketing zone, member portal zone, and Django admin.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.portal.urls')),
    path('', include('apps.public.urls')),
]
