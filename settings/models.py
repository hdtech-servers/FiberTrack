from django.db import models

class OrganizationSettings(models.Model):
    # Organization information
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='organization_logos/', null=True, blank=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Mpesa Daraja API Settings (reduced to required fields only)
    mpesa_consumer_key = models.CharField(max_length=255, null=True, blank=True)
    mpesa_consumer_secret = models.CharField(max_length=255, null=True, blank=True)
    mpesa_short_code = models.CharField(max_length=10, null=True, blank=True)
    mpesa_passkey = models.CharField(max_length=255, null=True, blank=True)
    mpesa_environment = models.CharField(
        max_length=10,
        choices=[('sandbox', 'Sandbox'), ('production', 'Production')],
        default='production'
    )

    # Secure SSL/TLS Email Server Settings
    smtp_host = models.CharField(max_length=255, null=True, blank=True)
    smtp_port = models.PositiveIntegerField(null=True, blank=True)
    smtp_use_tls = models.BooleanField(default=False)
    smtp_use_ssl = models.BooleanField(default=True)
    smtp_username = models.EmailField(null=True, blank=True)
    smtp_password = models.CharField(max_length=255, null=True, blank=True)
    smtp_from_email = models.EmailField(null=True, blank=True)

    # IMAP and POP3 Ports for Incoming Mail
    imap_port = models.PositiveIntegerField(default=993)
    pop3_port = models.PositiveIntegerField(default=995)

    google_maps_api_key = models.CharField(max_length=255, null=True, blank=True)

    # Theme settings
    theme = models.CharField(max_length=50, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')

    # Customization settings
    customer_prefix = models.CharField(max_length=10, blank=True, null=True, help_text="Prefix for customer IDs")
    employee_prefix = models.CharField(max_length=10, blank=True, null=True, help_text="Prefix for employee IDs")
    invoice_prefix = models.CharField(max_length=10, blank=True, null=True, help_text="Prefix for invoice numbers")
    quote_prefix = models.CharField(max_length=10, blank=True, null=True, help_text="Prefix for quote numbers")

    invoice_number_format = models.CharField(
        max_length=20, blank=True, null=True, help_text="Format for invoice numbering, e.g., INV-{number}"
    )
    quote_number_format = models.CharField(
        max_length=20, blank=True, null=True, help_text="Format for quote numbering, e.g., QTE-{number}"
    )

    quote_notes = models.TextField(blank=True, null=True, help_text="Default notes to be attached to quotes")
    invoice_notes = models.TextField(blank=True, null=True, help_text="Default notes to be attached to invoices")

    def __str__(self):
        return self.name
