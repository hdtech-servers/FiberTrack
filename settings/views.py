from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import OrganizationSettings
from .forms import (
    OrganizationInfoForm, DarajaAPIForm, EmailServerForm, GoogleAPISettingsForm,
    InvoiceSettingsForm, QuotationSettingsForm, CustomerSettingsForm, EmployeeSettingsForm
)

@login_required(login_url='/auth_app/login/')
def settings_view(request):
    organization_settings = OrganizationSettings.objects.first()
    if not organization_settings:
        organization_settings = OrganizationSettings.objects.create()

    context = {
        'organization': organization_settings,
        'organization_info_form': OrganizationInfoForm(instance=organization_settings),
        'daraja_api_form': DarajaAPIForm(instance=organization_settings),
        'email_server_form': EmailServerForm(instance=organization_settings),
        'google_api_form': GoogleAPISettingsForm(instance=organization_settings),
        'invoice_settings_form': InvoiceSettingsForm(instance=organization_settings),
        'quotation_settings_form': QuotationSettingsForm(instance=organization_settings),
        'customer_settings_form': CustomerSettingsForm(instance=organization_settings),
        'employee_settings_form': EmployeeSettingsForm(instance=organization_settings),
    }
    return render(request, 'settings/settings_view.html', context)

@login_required(login_url='/auth_app/login/')
def edit_organization_info(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = OrganizationInfoForm(request.POST, request.FILES, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization information updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth_app/login/')
def edit_daraja_api(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = DarajaAPIForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Daraja API settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth_app/login/')
def edit_email_server(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = EmailServerForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Email server settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth_app/login/')
def edit_google_api(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = GoogleAPISettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Google API settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth_app/login/')
def edit_invoice_settings(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = InvoiceSettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Invoice settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth_app/login/')
def edit_quotation_settings(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = QuotationSettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Quotation settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth_app/login/')
def edit_customer_settings(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = CustomerSettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth_app/login/')
def edit_employee_settings(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = EmployeeSettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee settings updated successfully.")
    return redirect('settings_view')
