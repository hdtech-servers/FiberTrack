from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Custom login view
    path('login/', views.custom_login, name='login'),

    # Logout view
    path('logout/', views.custom_logout, name='logout'),

    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # Password change view
    path('password_change/', views.change_password, name='password_change'),

    # User management views
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),

    # Profile views
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
