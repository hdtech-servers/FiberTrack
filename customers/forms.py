from django import forms
from .models import Customer

# Customer Form for Add/Edit Customer
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_number', 'email', 'pppoe_username', 'pppoe_password', 'billing_address', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['pppoe_username'].widget.attrs['readonly'] = True  # PPPoE username auto-generated but editable

# Import Customers Form
class CustomerImportForm(forms.Form):
    file = forms.FileField(label='Select a CSV file for import')

# Export Customers Form (empty, but allows for possible future extension)
class CustomerExportForm(forms.Form):
    pass
