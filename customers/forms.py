from django import forms

from services.models import SubscriptionPlan
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'contact_number', 'email', 'pppoe_username', 'pppoe_password',
            'billing_address', 'coordinates', 'account_balance', 'credit', 'outstanding_amount'
        ]

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['credit'].widget.attrs['readonly'] = True  # Credit is derived from balance
        self.fields['outstanding_amount'].widget.attrs['readonly'] = True  # Outstanding amount is derived from balance

    def clean(self):
        cleaned_data = super().clean()
        account_balance = cleaned_data.get('account_balance', 0)

        # Set credit and outstanding based on account balance
        if account_balance >= 0:
            cleaned_data['credit'] = account_balance
            cleaned_data['outstanding_amount'] = 0
        else:
            cleaned_data['credit'] = 0
            cleaned_data['outstanding_amount'] = -account_balance

        # Validate coordinates format if provided
        coordinates = cleaned_data.get('coordinates', None)
        if coordinates:
            try:
                lat_str, lon_str = coordinates.split(',')
                latitude = float(lat_str.strip())
                longitude = float(lon_str.strip())

                if not (-90 <= latitude <= 90):
                    self.add_error('coordinates', "Latitude must be between -90 and 90.")
                if not (-180 <= longitude <= 180):
                    self.add_error('coordinates', "Longitude must be between -180 and 180.")
            except ValueError:
                self.add_error('coordinates', "Coordinates must be in 'latitude,longitude' format.")

        return cleaned_data


# Import Customers Form
class CustomerImportForm(forms.Form):
    file = forms.FileField(label='Select a CSV file for import')


# Export Customers Form (empty, but allows for possible future extension)
class CustomerExportForm(forms.Form):
    pass


class AssignSubscriptionPlanForm(forms.ModelForm):
    subscription_plan = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Assign Subscription Plan"
    )

    class Meta:
        model = Customer
        fields = ['subscription_plan']