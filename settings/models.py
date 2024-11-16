from django.db import models

class OrganizationSettings(models.Model):
    # Basic Organization Info
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='organization_logos/', null=True, blank=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # M-Pesa Credentials and Environment Selection
    mpesa_consumer_key = models.CharField(max_length=255, null=True, blank=True)
    mpesa_consumer_secret = models.CharField(max_length=255, null=True, blank=True)
    mpesa_short_code = models.CharField(max_length=10, null=True, blank=True)
    mpesa_passkey = models.CharField(max_length=255, null=True, blank=True)
    mpesa_environment = models.CharField(
        max_length=10,
        choices=[('sandbox', 'Sandbox'), ('production', 'Production')],
        default='production',
        help_text="Select environment for Mpesa API"
    )

    # C2B (Customer to Business) URLs
    mpesa_validation_url_sandbox = models.URLField(null=True, blank=True, help_text="Sandbox validation URL")
    mpesa_validation_url_production = models.URLField(null=True, blank=True, help_text="Production validation URL")
    mpesa_confirmation_url_sandbox = models.URLField(null=True, blank=True, help_text="Sandbox confirmation URL")
    mpesa_confirmation_url_production = models.URLField(null=True, blank=True, help_text="Production confirmation URL")
    mpesa_response_type = models.CharField(max_length=10, choices=[('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Completed')
    mpesa_account_reference = models.CharField(max_length=50, null=True, blank=True)
    mpesa_transaction_desc = models.CharField(max_length=100, null=True, blank=True)

    # B2C (Business to Customer) Fields
    mpesa_b2c_short_code = models.CharField(max_length=10, null=True, blank=True)
    mpesa_b2c_initiator_name = models.CharField(max_length=50, null=True, blank=True)
    mpesa_b2c_security_credential = models.CharField(max_length=255, null=True, blank=True)
    mpesa_b2c_command_id = models.CharField(
        max_length=50,
        choices=[('BusinessPayment', 'BusinessPayment'), ('SalaryPayment', 'SalaryPayment'), ('PromotionPayment', 'PromotionPayment')],
        default='BusinessPayment'
    )
    mpesa_b2c_queue_timeout_url_sandbox = models.URLField(null=True, blank=True, help_text="Sandbox B2C timeout URL")
    mpesa_b2c_queue_timeout_url_production = models.URLField(null=True, blank=True, help_text="Production B2C timeout URL")
    mpesa_b2c_result_url_sandbox = models.URLField(null=True, blank=True, help_text="Sandbox B2C result URL")
    mpesa_b2c_result_url_production = models.URLField(null=True, blank=True, help_text="Production B2C result URL")

    # B2B (Business to Business) Fields
    mpesa_b2b_initiator_name = models.CharField(max_length=50, null=True, blank=True)
    mpesa_b2b_security_credential = models.CharField(max_length=255, null=True, blank=True)
    mpesa_b2b_short_code = models.CharField(max_length=10, null=True, blank=True)
    mpesa_b2b_receiver_party = models.CharField(max_length=10, null=True, blank=True, help_text="Receiver shortcode or till number")
    mpesa_b2b_command_id = models.CharField(
        max_length=50,
        choices=[('BusinessPayBill', 'BusinessPayBill'), ('BusinessBuyGoods', 'BusinessBuyGoods')],
        default='BusinessPayBill'
    )
    mpesa_b2b_queue_timeout_url_sandbox = models.URLField(null=True, blank=True, help_text="Sandbox B2B timeout URL")
    mpesa_b2b_queue_timeout_url_production = models.URLField(null=True, blank=True, help_text="Production B2B timeout URL")
    mpesa_b2b_result_url_sandbox = models.URLField(null=True, blank=True, help_text="Sandbox B2B result URL")
    mpesa_b2b_result_url_production = models.URLField(null=True, blank=True, help_text="Production B2B result URL")

    # Email Server Settings
    smtp_host = models.CharField(max_length=255, null=True, blank=True)
    smtp_port = models.PositiveIntegerField(null=True, blank=True, default=587)
    smtp_use_tls = models.BooleanField(default=True)
    smtp_use_ssl = models.BooleanField(default=False)
    smtp_username = models.EmailField(null=True, blank=True)
    smtp_password = models.CharField(max_length=255, null=True, blank=True)

    # Add these fields if they are needed
    smtp_from_email = models.EmailField(null=True, blank=True)
    imap_port = models.PositiveIntegerField(default=993, null=True, blank=True)
    pop3_port = models.PositiveIntegerField(default=995, null=True, blank=True)

    # Additional Organization Customizations
    theme = models.CharField(max_length=50, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    google_maps_api_key = models.CharField(max_length=255, null=True, blank=True)

    # Document Customization and Numbering Prefixes
    customer_prefix = models.CharField(max_length=10, blank=True, null=True)
    employee_prefix = models.CharField(max_length=10, blank=True, null=True)
    invoice_prefix = models.CharField(max_length=10, blank=True, null=True)
    quote_prefix = models.CharField(max_length=10, blank=True, null=True)
    invoice_number_format = models.CharField(max_length=20, blank=True, null=True)
    quote_number_format = models.CharField(max_length=20, blank=True, null=True)
    quote_notes = models.TextField(blank=True, null=True)
    invoice_notes = models.TextField(blank=True, null=True)

    def get_validation_url(self):
        return self.mpesa_validation_url_sandbox if self.mpesa_environment == 'sandbox' else self.mpesa_validation_url_production

    def get_confirmation_url(self):
        return self.mpesa_confirmation_url_sandbox if self.mpesa_environment == 'sandbox' else self.mpesa_confirmation_url_production

    def get_b2c_timeout_url(self):
        return self.mpesa_b2c_queue_timeout_url_sandbox if self.mpesa_environment == 'sandbox' else self.mpesa_b2c_queue_timeout_url_production

    def get_b2c_result_url(self):
        return self.mpesa_b2c_result_url_sandbox if self.mpesa_environment == 'sandbox' else self.mpesa_b2c_result_url_production

    def get_b2b_timeout_url(self):
        return self.mpesa_b2b_queue_timeout_url_sandbox if self.mpesa_environment == 'sandbox' else self.mpesa_b2b_queue_timeout_url_production

    def get_b2b_result_url(self):
        return self.mpesa_b2b_result_url_sandbox if self.mpesa_environment == 'sandbox' else self.mpesa_b2b_result_url_production

    def __str__(self):
        return self.name
