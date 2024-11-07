from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('add/', views.customer_add, name='customer_add'),  # Place this before customer_detail
    path('customer/<str:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/edit/<str:customer_id>/', views.customer_edit, name='customer_edit'),
    path('customers/import/', views.customer_import, name='customer_import'),
    path('customers/export/', views.customer_export, name='customer_export'),
    path('customers/delete/<str:customer_id>/', views.customer_delete, name='customer_delete'),
]
