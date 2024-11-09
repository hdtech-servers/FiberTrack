from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from services.models import SubscriptionPlan

# Invoice model
class Invoice(models.Model):
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

    def __str__(self):
        return f"Invoice {self.id} for Customer {self.customer.customer_id}"


# Quotation model
class Quotation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, to_field='customer_id')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    time_added = models.DateTimeField(auto_now_add=True)  # New field


    def __str__(self):
        return f"Quotation {self.id} for Customer {self.customer.customer_id}"

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
        return f"Payment {self.payment_id} for Invoice {self.invoice.id}"
