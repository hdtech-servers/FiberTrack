from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, Quotation, CustomItem, Payment

# Invoice Form
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'subscription_plan', 'amount_due', 'products_total',
                  'installation_fee', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'amount_due': forms.NumberInput(attrs={'step': '0.01'}),
            'products_total': forms.NumberInput(attrs={'step': '0.01'}),
            'installation_fee': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_due'].label = "Amount Due (KSH)"
        self.fields['products_total'].label = "Products Total (KSH)"
        self.fields['installation_fee'].label = "Installation Fee (KSH)"


# Quotation Form
class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['status']
        widgets = {'status': forms.Select()}


# Custom Item Form for Items within Quotations
class CustomItemForm(forms.ModelForm):
    class Meta:
        model = CustomItem
        fields = ['item_name', 'item_description', 'quantity', 'unit', 'price']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'step': '1', 'min': '1', 'value': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].initial = 1  # Default quantity to 1 if not provided
        self.fields['price'].initial = 0.00  # Default price to 0.00 if not provided


# Inline formset for Custom Items within Quotation
CustomItemFormSet = inlineformset_factory(
    Quotation,
    CustomItem,
    form=CustomItemForm,
    extra=1,  # Adjusts the number of empty forms to display
    can_delete=True  # Allows deletion of individual items in the formset
)


# Payment Form
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['invoice', 'payment_method', 'transaction_id', 'amount_paid', 'processed_by']
        widgets = {
            'amount_paid': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_paid'].label = "Amount Paid (KSH)"
