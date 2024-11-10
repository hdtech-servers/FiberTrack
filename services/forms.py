from django import forms
from .models import SubscriptionPlan

class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = [
            'name', 'download_speed', 'upload_speed', 'price', 'installation_fee',
            'plan_type', 'duration', 'time_unit', 'data_cap'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'download_speed': forms.TextInput(attrs={'class': 'form-control'}),
            'upload_speed': forms.TextInput(attrs={'class': 'form-control'}),  # Corrected field
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'installation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'plan_type': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'time_unit': forms.Select(attrs={'class': 'form-control'}),
            'data_cap': forms.TextInput(attrs={'class': 'form-control'}),
        }
