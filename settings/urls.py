from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings_view, name='settings_view'),
    path('settings/edit-organization-info/', views.edit_organization_info, name='edit_organization_info'),
    path('settings/edit-mpesa-c2b/', views.edit_mpesa_c2b, name='edit_mpesa_c2b'),
    path('settings/edit-mpesa-b2c/', views.edit_mpesa_b2c, name='edit_mpesa_b2c'),
    path('settings/edit-mpesa-b2b/', views.edit_mpesa_b2b, name='edit_mpesa_b2b'),
    path('settings/edit-email-server/', views.edit_email_server, name='edit_email_server'),
    path('settings/edit-customization/', views.edit_customization_settings, name='edit_customization_settings'),
]
