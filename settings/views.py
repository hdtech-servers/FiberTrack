from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import OrganizationSettings
from .forms import (
    OrganizationInfoForm, MpesaC2BSettingsForm, MpesaB2CSettingsForm, MpesaB2BSettingsForm,
    EmailServerSettingsForm, CustomizationSettingsForm
)

@login_required(login_url='/auth/login/')
def settings_view(request):
    """Display all settings with forms initialized with existing data."""
    organization_settings = OrganizationSettings.objects.first()
    if not organization_settings:
        organization_settings = OrganizationSettings.objects.create()  # Initialize settings if not present

    context = {
        'organization': organization_settings,
        'organization_info_form': OrganizationInfoForm(instance=organization_settings),
        'mpesa_c2b_form': MpesaC2BSettingsForm(instance=organization_settings),
        'mpesa_b2c_form': MpesaB2CSettingsForm(instance=organization_settings),
        'mpesa_b2b_form': MpesaB2BSettingsForm(instance=organization_settings),
        'email_server_form': EmailServerSettingsForm(instance=organization_settings),
        'customization_form': CustomizationSettingsForm(instance=organization_settings),
    }
    return render(request, 'settings/settings_view.html', context)

@login_required(login_url='/auth/login/')
def edit_organization_info(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = OrganizationInfoForm(request.POST, request.FILES, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization information updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth/login/')
def edit_mpesa_c2b(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = MpesaC2BSettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "M-Pesa C2B settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth/login/')
def edit_mpesa_b2c(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = MpesaB2CSettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "M-Pesa B2C settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth/login/')
def edit_mpesa_b2b(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = MpesaB2BSettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "M-Pesa B2B settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth/login/')
def edit_email_server(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = EmailServerSettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Email server settings updated successfully.")
    return redirect('settings_view')

@login_required(login_url='/auth/login/')
def edit_customization_settings(request):
    organization_settings = OrganizationSettings.objects.first()
    if request.method == 'POST':
        form = CustomizationSettingsForm(request.POST, instance=organization_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Customization settings updated successfully.")
    return redirect('settings_view')
