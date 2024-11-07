from django import forms
from .models import Invoice, Quotation, CustomItem, Payment
from django.forms import inlineformset_factory

# Invoice Form
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'subscription_plan', 'amount_due', 'products_total', 'installation_fee', 'due_date', 'status']
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

CustomItemFormSet = inlineformset_factory(
    Quotation,
    CustomItem,
    form=forms.ModelForm,
    fields=['item_name', 'item_description', 'quantity', 'unit', 'price'],
    extra=1,
    can_delete=True
)


# Custom Item Form
class CustomItemForm(forms.ModelForm):
    class Meta:
        model = CustomItem
        fields = ['item_name', 'item_description', 'quantity', 'unit', 'price']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'step': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].label = "Item Price (KSH)"
        self.fields['quantity'].label = "Quantity"

# Inline formset for Custom Items in Quotation
CustomItemFormSet = inlineformset_factory(
    Quotation,
    CustomItem,
    form=CustomItemForm,
    extra=1,
    can_delete=True,
)

# Payment Form
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['invoice', 'payment_method', 'transaction_id', 'amount_paid', 'processed_by']
        widgets = {
            'amount_paid': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_paid'].label = "Amount Paid (KSH)"
