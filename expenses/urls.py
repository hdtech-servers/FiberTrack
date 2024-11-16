from django.urls import path
from . import views

urlpatterns = [
    # Dashboard view
    path('dashboard/', views.dashboard, name='expense_dashboard'),
    path('api/expense-trend/', views.expense_trend_data, name='expense_trend_data'),

    # Expense CRUD views with pagination
    path('expenses/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.create_expense, name='create_expense'),
    path('expenses/edit/<int:expense_id>/', views.update_expense, name='update_expense'),
    path('expenses/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),

    # Expense Category CRUD views with pagination
    path('categories/', views.category_list, name='expense_category_list'),
    path('categories/add/', views.create_category, name='create_category'),
    path('categories/edit/<int:category_id>/', views.update_category, name='update_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    # Budget views
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.create_budget, name='create_budget'),

    # Payment Integration Views
    path('expenses/initiate_b2c_payment/<int:expense_id>/', views.initiate_b2c_payment, name='initiate_b2c_payment'),
    path('expenses/initiate_b2b_payment/<int:expense_id>/', views.initiate_b2b_payment, name='initiate_b2b_payment'),

    path('mpesa/b2c/result/', views.b2c_result_callback, name='b2c_result_callback'),
    path('mpesa/b2b/result/', views.b2b_result_callback, name='b2b_result_callback'),

    # Log View
    path('logs/', views.expense_log_list, name='expense_log_list'),

]
