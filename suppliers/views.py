from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Supplier
from .forms import SupplierForm
from django.core.paginator import Paginator


@login_required(login_url='/auth/login/')
def supplier_list(request):
    query = request.GET.get('q')
    suppliers = Supplier.objects.all().order_by('name')

    if query:
        suppliers = suppliers.filter(name__icontains=query)

    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    add_supplier_form = SupplierForm()
    edit_supplier_forms = {supplier.supplier_id: SupplierForm(instance=supplier) for supplier in suppliers}

    return render(request, 'suppliers/supplier_list.html', {
        'page_obj': page_obj,
        'query': query,
        'add_supplier_form': add_supplier_form,
        'edit_supplier_forms': edit_supplier_forms,
    })


@login_required(login_url='/auth/login/')
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
        else:
            # Handle form errors in case of invalid data
            return render(request, 'suppliers/add_supplier.html', {'form': form})

    return render(request, 'suppliers/add_supplier.html', {'form': SupplierForm()})


@login_required(login_url='/auth/login/')
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
        else:
            # Handle form errors for inline editing
            if request.is_ajax():
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = SupplierForm(instance=supplier)

    if request.is_ajax():
        # Return the supplier data as JSON for AJAX editing
        supplier_data = {
            'name': supplier.name,
            'contact_person': supplier.contact_person,
            'phone': supplier.phone,
            'email': supplier.email,
            'address': supplier.address,
            'city': supplier.city,
            'country': supplier.country,
            'notes': supplier.notes,
            'payment_method': supplier.payment_method,
            'paybill_number': supplier.paybill_number,
            'account_number': supplier.account_number,
            'till_number': supplier.till_number,
            'phone_payment_number': supplier.phone_payment_number,
        }
        return JsonResponse(supplier_data)

    return render(request, 'suppliers/edit_supplier.html', {'form': form, 'supplier': supplier})


@login_required(login_url='/auth/login/')
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return redirect('supplier_list')


@login_required(login_url='/auth/login/')
def view_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    return render(request, 'suppliers/view_supplier.html', {'supplier': supplier})
