from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name','last_name', 'contact_number', 'email', 'pppoe_username', 'pppoe_password',
            'billing_address', 'latitude', 'longitude', 'account_balance', 'credit', 'outstanding_amount'
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

        return cleaned_data


# Import Customers Form
class CustomerImportForm(forms.Form):
    file = forms.FileField(label='Select a CSV file for import')


# Export Customers Form (empty, but allows for possible future extension)
class CustomerExportForm(forms.Form):
    pass
