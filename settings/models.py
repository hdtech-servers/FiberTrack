from django.db import models

class OrganizationSettings(models.Model):
    # Organization information
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='organization_logos/', null=True, blank=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Mpesa Daraja API Settings
    mpesa_consumer_key = models.CharField(max_length=255, null=True, blank=True)
    mpesa_consumer_secret = models.CharField(max_length=255, null=True, blank=True)
    mpesa_short_code = models.CharField(max_length=10, null=True, blank=True)
    mpesa_initiator_username = models.CharField(max_length=255, null=True, blank=True)
    mpesa_security_credential = models.TextField(null=True, blank=True)
    mpesa_passkey = models.CharField(max_length=255, null=True, blank=True)
    mpesa_transaction_type = models.CharField(max_length=50, default='CustomerPayBillOnline')
    mpesa_callback_url = models.URLField(max_length=500, null=True, blank=True)
    mpesa_confirmation_url = models.URLField(max_length=500, null=True, blank=True)
    mpesa_validation_url = models.URLField(max_length=500, null=True, blank=True)
    mpesa_timeout_url = models.URLField(max_length=500, null=True, blank=True)
    mpesa_result_url = models.URLField(max_length=500, null=True, blank=True)
    mpesa_environment = models.CharField(max_length=10, choices=[('sandbox', 'Sandbox'), ('production', 'Production')], default='sandbox')

    # TextSMS API Settings
    textsms_api_key = models.CharField(max_length=255, null=True, blank=True)
    textsms_sender_id = models.CharField(max_length=255, null=True, blank=True)
    textsms_url = models.URLField(max_length=500, null=True, blank=True)

    # Google Maps API
    google_maps_api_key = models.CharField(max_length=255, null=True, blank=True)

    # SMTP Email Server Settings
    smtp_host = models.CharField(max_length=255, null=True, blank=True)
    smtp_port = models.PositiveIntegerField(null=True, blank=True)
    smtp_use_tls = models.BooleanField(default=True)
    smtp_use_ssl = models.BooleanField(default=False)
    smtp_username = models.CharField(max_length=255, null=True, blank=True)
    smtp_password = models.CharField(max_length=255, null=True, blank=True)
    smtp_from_email = models.EmailField(null=True, blank=True)

    # Theme settings
    theme = models.CharField(max_length=50, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')

    def __str__(self):
        return self.name
