from django.urls import path
from . import views

urlpatterns = [
    path('', views.settings_view, name='settings_view'),
    path('edit/organization-info/', views.edit_organization_info, name='edit_organization_info'),
    path('edit/daraja-api/', views.edit_daraja_api, name='edit_daraja_api'),
    path('edit/email-server/', views.edit_email_server, name='edit_email_server'),
    path('edit/google-api/', views.edit_google_api, name='edit_google_api'),
    path('edit/invoice-settings/', views.edit_invoice_settings, name='edit_invoice_settings'),
    path('edit/quotation-settings/', views.edit_quotation_settings, name='edit_quotation_settings'),
    path('edit/customer-settings/', views.edit_customer_settings, name='edit_customer_settings'),
    path('edit/employee-settings/', views.edit_employee_settings, name='edit_employee_settings'),
]
