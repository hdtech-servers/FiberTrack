from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .forms import InventoryForm, SupplierForm
from .models import InventoryItem, Supplier
from django.db.models import Q  # For search functionality

# Inventory Item Views
class InventoryListView(ListView):
    model = InventoryItem
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'items'
    paginate_by = 25  # Pagination size

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = InventoryItem.objects.all()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(supplier__name__icontains=search_query)
            )
        return queryset

class InventoryCreateView(CreateView):
    model = InventoryItem
    form_class = InventoryForm
    template_name = 'inventory/inventory_form.html'
    success_url = reverse_lazy('inventory_list')


class InventoryUpdateView(UpdateView):
    model = InventoryItem
    template_name = 'inventory/inventory_form.html'
    fields = ['name', 'description', 'quantity', 'cost', 'supplier', 'low_stock_alert_threshold']
    success_url = reverse_lazy('inventory_list')

class InventoryDetailView(DetailView):
    model = InventoryItem
    template_name = 'inventory/inventory_detail.html'
    context_object_name = 'item'

class InventoryDeleteView(DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory_list')

# Supplier Views
class SupplierListView(ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 25  # Pagination size

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = Supplier.objects.all()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(contact_info__icontains=search_query)
            )
        return queryset

class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierUpdateView(UpdateView):
    model = Supplier
    template_name = 'inventory/supplier_form.html'
    fields = ['name', 'contact_info', 'email', 'phone', 'address']
    success_url = reverse_lazy('supplier_list')

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'inventory/supplier_detail.html'
    context_object_name = 'supplier'

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'inventory/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier_list')
