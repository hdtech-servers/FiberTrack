from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from services.models import SubscriptionPlan
from settings.models import OrganizationSettings

# Invoice model
class Invoice(models.Model):
    invoice_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, to_field='customer_id')
    subscription_plan = models.ForeignKey('services.SubscriptionPlan', on_delete=models.CASCADE, null=True, blank=True)  # Optional
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    products_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    installation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)  # Optional
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Overdue', 'Overdue')]
    )

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            # Retrieve prefix from settings or use a default
            prefix = "INV-"
            try:
                organization_settings = OrganizationSettings.objects.first()
                if organization_settings and organization_settings.invoice_prefix:
                    prefix = organization_settings.invoice_prefix
            except OrganizationSettings.DoesNotExist:
                pass  # Fallback to default prefix

            # Generate a six-digit sequential ID with the prefix
            last_invoice = Invoice.objects.filter(invoice_id__startswith=prefix).order_by('-invoice_id').first()
            if last_invoice:
                last_id = int(last_invoice.invoice_id.replace(prefix, ''))
                new_id = last_id + 1
            else:
                new_id = 1

            self.invoice_id = f"{prefix}{new_id:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_id} for Customer {self.customer.customer_id}"


# Quotation model
class Quotation(models.Model):
    quotation_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, to_field='customer_id')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    time_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.quotation_id:
            # Retrieve prefix from settings or use a default
            prefix = "QTE-"
            try:
                organization_settings = OrganizationSettings.objects.first()
                if organization_settings and organization_settings.quote_prefix:
                    prefix = organization_settings.quote_prefix
            except OrganizationSettings.DoesNotExist:
                pass  # Fallback to default prefix

            # Generate a six-digit sequential ID with the prefix
            last_quotation = Quotation.objects.filter(quotation_id__startswith=prefix).order_by('-quotation_id').first()
            if last_quotation:
                last_id = int(last_quotation.quotation_id.replace(prefix, ''))
                new_id = last_id + 1
            else:
                new_id = 1

            self.quotation_id = f"{prefix}{new_id:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Quotation {self.quotation_id} for Customer {self.customer.customer_id}"


# Custom Item model
class CustomItem(models.Model):
    quotation = models.ForeignKey(Quotation, related_name='items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.item_name} - {self.quantity} {self.unit} at {self.price} each"


# Payment model to track payments made towards invoices
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('Mpesa', 'Mpesa'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    )

    payment_id = models.CharField(max_length=6, unique=True, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            last_payment = Payment.objects.all().order_by('id').last()
            if last_payment:
                new_id = int(last_payment.payment_id) + 1
                self.payment_id = f"{new_id:06d}"
            else:
                self.payment_id = "000001"
        super(Payment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Payment {self.payment_id} for Invoice {self.invoice.invoice_id}"
