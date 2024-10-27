from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('customers/<str:customer_id>/', views.customer_detail, name='customer_detail'),
    path('add/', views.customer_add, name='customer_add'),
    path('customers/edit/<str:customer_id>/', views.customer_edit, name='customer_edit'),  # Ensure this pattern is correct
    path('customers/import/', views.customer_import, name='customer_import'),
    path('customers/export/', views.customer_export, name='customer_export'),  # Add export URL
    path('customers/delete/<str:customer_id>/', views.customer_delete, name='customer_delete'),  # Add delete URL

]
