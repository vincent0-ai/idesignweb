"""
URL configuration for idesignweb public marketing zone.
"""

from django.urls import path
from apps.public import views

app_name = 'public'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('services/', views.services_hub_view, name='services_hub'),
    path('services/<slug:slug>/', views.service_detail_view, name='service_detail'),
    path('work/', views.work_list_view, name='work_list'),
    path('work/<slug:slug>/', views.work_detail_view, name='work_detail'),
    path('about/', views.about_view, name='about'),
    path('insights/', views.insights_list_view, name='insights_list'),
    path('insights/<slug:slug>/', views.insight_detail_view, name='insight_detail'),
    path('contact/', views.contact_view, name='contact'),
]
