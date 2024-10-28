from django.shortcuts import render, redirect
from .models import OrganizationSettings
from .forms import OrganizationSettingsForm


def settings_view(request):
    settings = OrganizationSettings.objects.first()

    if request.method == 'POST':
        form = OrganizationSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('settings_view')
    else:
        form = OrganizationSettingsForm(instance=settings)

    return render(request, 'settings/settings_form.html', {'form': form})

def view_edit_organization(request):
    # Fetch the first OrganizationSettings instance (assuming there's only one)
    organization_settings = OrganizationSettings.objects.first()

    if request.method == 'POST':
        # Handle form submission for editing
        form = OrganizationSettingsForm(request.POST, request.FILES, instance=organization_settings)
        if form.is_valid():
            form.save()
            return redirect('view_edit_organization')
    else:
        # Display the current organization settings in the form
        form = OrganizationSettingsForm(instance=organization_settings)

    # Pass the current organization and form to the template
    return render(request, 'settings/view_edit_organization.html', {
        'organization': organization_settings,
        'form': form
    })