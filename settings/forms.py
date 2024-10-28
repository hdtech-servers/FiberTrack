from django import forms
from .models import OrganizationSettings


class OrganizationSettingsForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = [
            'name', 'logo', 'address', 'mpesa_consumer_key', 'mpesa_consumer_secret',
            'mpesa_short_code', 'mpesa_initiator_username', 'mpesa_security_credential',
            'mpesa_passkey', 'mpesa_callback_url', 'mpesa_environment',  # Mpesa environment added
            'smtp_host', 'smtp_port', 'smtp_username', 'smtp_password',
            'smtp_from_email', 'smtp_use_tls', 'smtp_use_ssl',
            'google_maps_api_key',  # Google Maps API key added
            'theme'
        ]
        widgets = {
            # Organization name: simple text input
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),

            # Logo: file input
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),

            # Address: textarea
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter the address'}),

            # Mpesa Fields: text inputs for API keys, shortcode
            'mpesa_consumer_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mpesa Consumer Key'}),
            'mpesa_consumer_secret': forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Mpesa Consumer Secret'}),
            'mpesa_short_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mpesa Shortcode'}),
            'mpesa_initiator_username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Initiator Username'}),
            'mpesa_security_credential': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Security Credential'}),
            'mpesa_passkey': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mpesa Passkey'}),
            'mpesa_callback_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Callback URL'}),

            # Mpesa Environment Selection (Sandbox/Production)
            'mpesa_environment': forms.Select(choices=[('sandbox', 'Sandbox'), ('production', 'Production')],
                                              attrs={'class': 'form-control'}),  # Environment selection widget

            # SMTP Email Fields
            'smtp_host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SMTP Host'}),
            'smtp_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'SMTP Port'}),
            'smtp_username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SMTP Username'}),
            'smtp_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'SMTP Password'}),
            'smtp_from_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'From Email'}),
            'smtp_use_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'smtp_use_ssl': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # Google Maps API
            'google_maps_api_key': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Google Maps API Key'}),

            # Theme selection
            'theme': forms.Select(attrs={'class': 'form-control'}),
        }
