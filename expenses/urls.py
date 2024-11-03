from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_expenses, name='list_expenses'),  # List all expenses
    path('add/', views.add_expense, name='add_expense'),  # Add new expense
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),  # Edit expense
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),  # Delete expense

    # Expense Category URLs
    path('categories/', views.expenses_category_list, name='expenses_category_list'),  # List and add categories
    path('categories/edit/<int:pk>/', views.expenses_category_edit, name='expenses_category_edit'),  # Edit category
    path('categories/delete/<int:pk>/', views.expenses_category_delete, name='expenses_category_delete'),  # Delete category
]
