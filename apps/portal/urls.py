"""
URL configuration for idesignweb member portal zone.
"""

from django.urls import path
from apps.portal import views

app_name = 'portal'

urlpatterns = [
    # Auth Endpoints
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Member Portal Gated Routes
    path('portal/', views.dashboard_view, name='dashboard'),
    path('portal/communications/', views.communications_view, name='communications'),
    path('portal/projects/', views.projects_view, name='projects'),
    path('portal/projects/<str:project_code>/', views.project_detail_view, name='project_detail'),
    path('portal/projects/<str:project_code>/deliverables/<str:deliverable_id>/', views.deliverable_action_view, name='deliverable_action'),
    path('portal/assets/', views.asset_library_view, name='assets'),
    path('portal/support/', views.tickets_view, name='tickets'),
    path('portal/support/new/', views.create_ticket_view, name='create_ticket'),
    path('portal/support/<str:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
]
