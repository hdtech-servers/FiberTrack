from django import forms
from .models import OrganizationSettings

class OrganizationInfoForm(forms.ModelForm):
    """Form for basic organization information."""
    class Meta:
        model = OrganizationSettings
        fields = ['name', 'logo', 'address', 'contact_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class MpesaC2BSettingsForm(forms.ModelForm):
    """Form for M-Pesa C2B settings."""
    class Meta:
        model = OrganizationSettings
        fields = [
            'mpesa_consumer_key', 'mpesa_consumer_secret', 'mpesa_short_code', 'mpesa_passkey', 'mpesa_environment',
            'mpesa_validation_url_sandbox', 'mpesa_validation_url_production', 'mpesa_confirmation_url_sandbox',
            'mpesa_confirmation_url_production', 'mpesa_response_type', 'mpesa_account_reference', 'mpesa_transaction_desc'
        ]
        widgets = {
            'mpesa_consumer_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'M-Pesa Consumer Key'}),
            'mpesa_consumer_secret': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'M-Pesa Consumer Secret'}),
            'mpesa_short_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short Code'}),
            'mpesa_passkey': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Passkey'}),
            'mpesa_environment': forms.Select(attrs={'class': 'form-control'}),
            'mpesa_validation_url_sandbox': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Sandbox Validation URL'}),
            'mpesa_validation_url_production': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Production Validation URL'}),
            'mpesa_confirmation_url_sandbox': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Sandbox Confirmation URL'}),
            'mpesa_confirmation_url_production': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Production Confirmation URL'}),
            'mpesa_response_type': forms.Select(attrs={'class': 'form-control'}),
            'mpesa_account_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Reference'}),
            'mpesa_transaction_desc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction Description'}),
        }

class MpesaB2CSettingsForm(forms.ModelForm):
    """Form for M-Pesa B2C settings."""
    class Meta:
        model = OrganizationSettings
        fields = [
            'mpesa_b2c_short_code', 'mpesa_b2c_initiator_name', 'mpesa_b2c_security_credential', 'mpesa_b2c_command_id',
            'mpesa_b2c_queue_timeout_url_sandbox', 'mpesa_b2c_queue_timeout_url_production',
            'mpesa_b2c_result_url_sandbox', 'mpesa_b2c_result_url_production'
        ]
        widgets = {
            'mpesa_b2c_short_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'B2C Short Code'}),
            'mpesa_b2c_initiator_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Initiator Name'}),
            'mpesa_b2c_security_credential': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Security Credential'}),
            'mpesa_b2c_command_id': forms.Select(attrs={'class': 'form-control'}),
            'mpesa_b2c_queue_timeout_url_sandbox': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Sandbox Timeout URL'}),
            'mpesa_b2c_queue_timeout_url_production': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Production Timeout URL'}),
            'mpesa_b2c_result_url_sandbox': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Sandbox Result URL'}),
            'mpesa_b2c_result_url_production': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Production Result URL'}),
        }

class MpesaB2BSettingsForm(forms.ModelForm):
    """Form for M-Pesa B2B settings."""
    class Meta:
        model = OrganizationSettings
        fields = [
            'mpesa_b2b_initiator_name', 'mpesa_b2b_security_credential', 'mpesa_b2b_short_code', 'mpesa_b2b_receiver_party',
            'mpesa_b2b_command_id', 'mpesa_b2b_queue_timeout_url_sandbox', 'mpesa_b2b_queue_timeout_url_production',
            'mpesa_b2b_result_url_sandbox', 'mpesa_b2b_result_url_production'
        ]
        widgets = {
            'mpesa_b2b_initiator_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Initiator Name'}),
            'mpesa_b2b_security_credential': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Security Credential'}),
            'mpesa_b2b_short_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'B2B Short Code'}),
            'mpesa_b2b_receiver_party': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Party'}),
            'mpesa_b2b_command_id': forms.Select(attrs={'class': 'form-control'}),
            'mpesa_b2b_queue_timeout_url_sandbox': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Sandbox Timeout URL'}),
            'mpesa_b2b_queue_timeout_url_production': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Production Timeout URL'}),
            'mpesa_b2b_result_url_sandbox': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Sandbox Result URL'}),
            'mpesa_b2b_result_url_production': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Production Result URL'}),
        }

class EmailServerSettingsForm(forms.ModelForm):
    """Form for email server settings."""
    class Meta:
        model = OrganizationSettings
        fields = [
            'smtp_host', 'smtp_port', 'smtp_use_tls', 'smtp_use_ssl', 'smtp_username', 'smtp_password',
            'smtp_from_email', 'imap_port', 'pop3_port'
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

class CustomizationSettingsForm(forms.ModelForm):
    """Form for theme, Google Maps API, and prefixes for IDs and documents."""
    class Meta:
        model = OrganizationSettings
        fields = [
            'theme', 'google_maps_api_key', 'customer_prefix', 'employee_prefix', 'invoice_prefix',
            'quote_prefix', 'invoice_number_format', 'quote_number_format', 'quote_notes', 'invoice_notes'
        ]
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'google_maps_api_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Google Maps API Key'}),
            'customer_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Prefix'}),
            'employee_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee Prefix'}),
            'invoice_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Prefix'}),
            'quote_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quote Prefix'}),
            'invoice_number_format': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Number Format'}),
            'quote_number_format': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quote Number Format'}),
            'quote_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Default Notes for Quotes'}),
            'invoice_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Default Notes for Invoices'}),
        }
