from django import forms
from .models import OrganizationSettings

class OrganizationInfoForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = ['name', 'logo', 'address', 'contact_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter the address'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        }

class DarajaAPIForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = ['mpesa_consumer_key', 'mpesa_consumer_secret', 'mpesa_short_code', 'mpesa_passkey']
        widgets = {
            'mpesa_consumer_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mpesa Consumer Key'}),
            'mpesa_consumer_secret': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mpesa Consumer Secret'}),
            'mpesa_short_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mpesa Shortcode'}),
            'mpesa_passkey': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mpesa Passkey'}),
        }

class EmailServerForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = [
            'smtp_host', 'smtp_port', 'smtp_username', 'smtp_password',
            'smtp_from_email', 'smtp_use_tls', 'smtp_use_ssl',
            'imap_port', 'pop3_port'
        ]
        widgets = {
            'smtp_host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SMTP Host'}),
            'smtp_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'SMTP Port'}),
            'smtp_username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SMTP Username'}),
            'smtp_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'SMTP Password'}),
            'smtp_from_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'From Email'}),
            'smtp_use_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'smtp_use_ssl': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imap_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'IMAP Port'}),
            'pop3_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'POP3 Port'}),
        }

class GoogleAPISettingsForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = ['google_maps_api_key']
        widgets = {
            'google_maps_api_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Google Maps API Key'}),
        }

class InvoiceSettingsForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = ['invoice_prefix', 'invoice_number_format', 'invoice_notes']
        widgets = {
            'invoice_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Prefix'}),
            'invoice_number_format': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Number Format'}),
            'invoice_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Default Notes for Invoices'}),
        }

class QuotationSettingsForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = ['quote_prefix', 'quote_number_format', 'quote_notes']
        widgets = {
            'quote_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quote Prefix'}),
            'quote_number_format': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quote Number Format'}),
            'quote_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Default Notes for Quotes'}),
        }

class CustomerSettingsForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = ['customer_prefix']
        widgets = {
            'customer_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Prefix'}),
        }

class EmployeeSettingsForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = ['employee_prefix']
        widgets = {
            'employee_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee Prefix'}),
        }
