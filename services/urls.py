# services/urls.py

from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.subscription_plan_list, name='subscription_plan_list'),
    path('plan/new/', views.subscription_plan_create, name='subscription_plan_create'),
    path('plan/<int:pk>/', views.subscription_plan_detail, name='subscription_plan_detail'),
    path('plan/<int:pk>/edit/', views.subscription_plan_edit, name='subscription_plan_edit'),
    path('plan/<int:pk>/delete/', views.subscription_plan_delete, name='subscription_plan_delete'),
]
