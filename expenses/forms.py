from django import forms
from .models import Expense, ExpenseCategory, Budget

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'category', 'supplier', 'date', 'amount', 'description',
            'payment_method', 'payment_status', 'payment_reference', 'receipt', 'is_recurring'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'payment_reference': forms.TextInput(attrs={'class': 'form-control'}),
            'receipt': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.supplier and self.instance.supplier.payment_method:
            self.fields['payment_method'].initial = self.instance.supplier.payment_method
            self.fields['payment_method'].widget.attrs['readonly'] = True

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'monthly_limit', 'year', 'month']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'monthly_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'month': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Month (1-12)'}),
        }


class ExpenseLogFilterForm(forms.Form):
    operation_choices = [
        ('', 'All Operations'),
        ('CREATE', 'Create'),
        ('READ', 'Read'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete')
    ]
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    operation = forms.ChoiceField(
        choices=operation_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
