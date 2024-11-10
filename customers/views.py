from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm, CustomerImportForm, AssignSubscriptionPlanForm
import csv
from django.http import HttpResponse
from settings.models import OrganizationSettings


@login_required(login_url='/auth_app/login/')
def customer_list(request):
    search_query = request.GET.get('q', '').strip()
    per_page = request.GET.get('per_page', 25)

    # Filter customers based on the search query
    customers = Customer.objects.all()
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(contact_number__icontains=search_query) |
            Q(pppoe_username__icontains=search_query)
        )

    paginator = Paginator(customers, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = CustomerForm()

    context = {
        'customers': page_obj,
        'form': form,
        'search_query': search_query,
        'per_page': per_page,
    }

    return render(request, 'customer_list.html', context)


@login_required(login_url='/auth_app/login/')
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)

    # Fetch organization settings for the Google Maps API key
    organization_settings = OrganizationSettings.objects.first()
    google_maps_api_key = organization_settings.google_maps_api_key if organization_settings else ""

    # Handle subscription plan assignment form
    if request.method == 'POST':
        form = AssignSubscriptionPlanForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscription plan assigned successfully.")
            return redirect('customer_detail', customer_id=customer.customer_id)
    else:
        form = AssignSubscriptionPlanForm(instance=customer)

    context = {
        'customer': customer,
        'google_maps_api_key': google_maps_api_key,
        'organization_settings': organization_settings,
        'recent_activity': [
            {"description": "Payment received", "date": customer.date_created, "amount": 50},
            {"description": "Invoice generated", "date": customer.date_created}
        ],
        'form': form,  # Add the form to the context
    }
    return render(request, 'customer_detail.html', context)
@login_required(login_url='/auth_app/login/')
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    customer.delete()
    return redirect('customer_list')


@login_required(login_url='/auth_app/login/')
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


@login_required(login_url='/auth_app/login/')
def customer_edit(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)

    # Fetch organization settings for the Google Maps API key
    organization_settings = OrganizationSettings.objects.first()
    google_maps_api_key = organization_settings.google_maps_api_key if organization_settings else ""

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            # Save form fields
            customer = form.save(commit=False)

            # Get latitude and longitude from the form
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            # Update customer coordinates if provided
            if latitude and longitude:
                customer.latitude = latitude
                customer.longitude = longitude

            # Save the customer instance
            customer.save()

            messages.success(request, "Customer details updated successfully!")
            return redirect('customer_detail', customer_id=customer.customer_id)
    else:
        form = CustomerForm(instance=customer)

    context = {
        'customer': customer,
        'form': form,
        'google_maps_api_key': google_maps_api_key,
    }
    return render(request, 'customer_edit.html', context)

@login_required(login_url='/auth_app/login/')
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
                first_name, last_name, contact_number, email, pppoe_username, pppoe_password, billing_address, coordinates = row
                Customer.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    contact_number=contact_number,
                    email=email,
                    pppoe_username=pppoe_username,
                    pppoe_password=pppoe_password,
                    billing_address=billing_address,
                    coordinates=coordinates
                )
            messages.success(request, "Customers imported successfully!")
            return redirect('customer_list')
    else:
        form = CustomerImportForm()
    return render(request, 'customer_list.html', {'form': form})


@login_required(login_url='/auth_app/login/')
def customer_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Customer ID', 'First Name', 'Last Name', 'Contact Number', 'Email', 'PPPoE Username', 'Billing Address', 'Coordinates'])

    customers = Customer.objects.all()
    for customer in customers:
        writer.writerow([customer.customer_id, customer.first_name, customer.last_name, customer.contact_number, customer.email, customer.pppoe_username, customer.billing_address, customer.coordinates])

    return response
