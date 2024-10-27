from django.urls import path
from .views import (
    InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDetailView, InventoryDeleteView,
    SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDetailView, SupplierDeleteView
)

urlpatterns = [
    # Inventory URLs
    path('/products/', InventoryListView.as_view(), name='inventory_list'),
    path('/product/add/', InventoryCreateView.as_view(), name='inventory_add'),
    path('/product/<int:pk>/', InventoryDetailView.as_view(), name='inventory_detail'),
    path('/product/<int:pk>/edit/', InventoryUpdateView.as_view(), name='inventory_edit'),
    path('/product/<int:pk>/delete/', InventoryDeleteView.as_view(), name='inventory_delete'),

    # Supplier URLs
    path('/suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('/supplier/add/', SupplierCreateView.as_view(), name='supplier_add'),
    path('/supplier/<int:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),
    path('/supplier/<int:pk>/edit/', SupplierUpdateView.as_view(), name='supplier_edit'),
    path('/supplier/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),
]
