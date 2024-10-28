from django import forms
from django.forms import modelformset_factory
from .models import Payment, SubscriptionPlan, Invoice, Quotation, CustomItem

# Payment Form
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['invoice', 'payment_method', 'transaction_id', 'amount_paid']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Quotation Form
class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['customer', 'subscription_plan', 'amount_due', 'products_total', 'installation_fee', 'due_date', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'subscription_plan': forms.Select(attrs={'class': 'form-control'}),
            'amount_due': forms.NumberInput(attrs={'class': 'form-control'}),
            'products_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'installation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

# Invoice Form
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'subscription_plan', 'amount_due', 'products_total', 'installation_fee', 'due_date', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'subscription_plan': forms.Select(attrs={'class': 'form-control'}),
            'amount_due': forms.NumberInput(attrs={'class': 'form-control'}),
            'products_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'installation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

# Custom Item Form
class CustomItemForm(forms.ModelForm):
    class Meta:
        model = CustomItem
        fields = ['item_name', 'item_description', 'item_price']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'item_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Formset for Custom Items
CustomItemFormSet = modelformset_factory(
    CustomItem,
    fields=('item_name', 'item_description', 'item_price'),
    extra=1,  # Allows at least one item to be added, more dynamically
    widgets={
        'item_name': forms.TextInput(attrs={'class': 'form-control'}),
        'item_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        'item_price': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)

# Subscription Plan Form
class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'bandwidth', 'price', 'installation_fee', 'plan_type', 'duration', 'time_unit', 'data_cap']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bandwidth': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'installation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'plan_type': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'time_unit': forms.Select(attrs={'class': 'form-control'}),
            'data_cap': forms.TextInput(attrs={'class': 'form-control'}),
        }
