from django import forms
from .models import Supplier
from django.core.exceptions import ValidationError


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name', 'contact_person', 'phone', 'email', 'address', 'city', 'country', 'notes',
            'payment_method', 'paybill_number', 'account_number', 'till_number', 'phone_payment_number'
        ]

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        # Validate that the necessary fields are provided based on payment method
        if payment_method == 'Paybill':
            if not cleaned_data.get('paybill_number') or not cleaned_data.get('account_number'):
                raise ValidationError("Paybill number and account number are required for Paybill payments.")
        elif payment_method == 'Till':
            if not cleaned_data.get('till_number'):
                raise ValidationError("Till number is required for Till (Buy Goods) payments.")
        elif payment_method == 'Phone':
            if not cleaned_data.get('phone_payment_number'):
                raise ValidationError("Phone number is required for Phone payments.")

        return cleaned_data
