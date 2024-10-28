from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer  # Assuming you have a customer app

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subscription_plan = models.CharField(max_length=100)  # Customize this as per your plan model
    billing_cycle = models.DateTimeField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    penalty_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.customer}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('Mpesa', 'Mpesa'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # For Mpesa payments
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Who processed the payment

    def __str__(self):
        return f"Payment {self.id} for Invoice {self.invoice.id}"
