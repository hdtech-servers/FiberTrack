from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm, CustomerImportForm
import csv
from django.http import HttpResponse

# List of Customers
def customer_list(request):
    # Get the search query from the GET request (case-insensitive)
    search_query = request.GET.get('q', '').strip()
    per_page = request.GET.get('per_page', 25)  # Get per page option, default to 25

    # Filter customers based on the search query
    customers = Customer.objects.all()

    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(contact_number__icontains=search_query) |
            Q(pppoe_username__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(customers, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Form for adding customers in the modal
    form = CustomerForm()

    context = {
        'customers': page_obj,
        'form': form,
        'search_query': search_query,
        'per_page': per_page,
    }

    return render(request, 'customer_list.html', context)

# Customer Details
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    return render(request, 'customer_detail.html', {'customer': customer})

def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    customer.delete()
    return redirect('customer_list')


# Add New Customer
def customer_add(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added successfully!")
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {'form': form})

# Edit Existing Customer
def customer_edit(request, customer_id):
    # Retrieve the customer object based on customer_id
    customer = get_object_or_404(Customer, customer_id=customer_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=customer.customer_id)
    else:
        form = CustomerForm(instance=customer)

    # Pass the customer and form to the template
    return render(request, 'customer_edit.html', {'form': form, 'customer': customer})
# Import Customers from CSV
def customer_import(request):
    if request.method == "POST":
        form = CustomerImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file')
                return redirect('customer_list')

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader)  # Skip header
            for row in reader:
                name, contact_number, email, pppoe_username, pppoe_password, billing_address, latitude, longitude = row
                latitude = latitude or None
                longitude = longitude or None
                Customer.objects.create(
                    name=name,
                    contact_number=contact_number,
                    email=email,
                    pppoe_username=pppoe_username,
                    pppoe_password=pppoe_password,
                    billing_address=billing_address,
                    latitude=latitude,
                    longitude=longitude
                )
            messages.success(request, "Customers imported successfully!")
            return redirect('customer_list')
    else:
        form = CustomerImportForm()
    return render(request, 'customer_list.html', {'form': form})

# Export Customers to CSV
def customer_export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Customer ID', 'Name', 'Contact Number', 'Email', 'PPPoE Username', 'Billing Address'])

    # Write data rows
    customers = Customer.objects.all()
    for customer in customers:
        writer.writerow([customer.customer_id, customer.name, customer.contact_number, customer.email, customer.pppoe_username, customer.billing_address])

    return response
