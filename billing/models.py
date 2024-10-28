from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer  # Assuming you have a customer app
from datetime import timedelta
from dateutil.relativedelta import relativedelta  # For handling months

# CustomItem model to be used for both quotations and invoices
class CustomItem(models.Model):
    invoice = models.ForeignKey('Invoice', related_name='items', on_delete=models.CASCADE, null=True, blank=True)  # Link to Invoice
    quotation = models.ForeignKey('Quotation', related_name='items', on_delete=models.CASCADE, null=True, blank=True)  # Link to Quotation
    item_name = models.CharField(max_length=100)  # Name of the custom item
    item_description = models.TextField(blank=True, null=True)  # Description of the item (optional)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the custom item

    def __str__(self):
        return f"{self.item_name} - {self.item_price}"

# SubscriptionPlan model to define service plans
class SubscriptionPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('pppoe', 'PPPoE and Hotspot Users'),
        ('hotspot', 'Hotspot Users Only'),
    ]

    TIME_UNIT_CHOICES = [
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ]

    name = models.CharField(max_length=100)  # Plan Name
    bandwidth = models.CharField(max_length=50)  # Bandwidth (e.g., 10 Mbps)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price
    installation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Installation fee
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES, default='pppoe')  # PPPoE or Hotspot
    duration = models.PositiveIntegerField()  # Input duration, e.g., "30"
    time_unit = models.CharField(max_length=10, choices=TIME_UNIT_CHOICES, default='days')  # Time unit: minutes, hours, etc.
    data_cap = models.CharField(max_length=50, null=True, blank=True)  # Data Cap (optional)

    def __str__(self):
        return f"{self.name} - {self.bandwidth} @ {self.price} for {self.duration} {self.time_unit}"

    def get_expiration_date(self, start_date):
        """
        Calculate expiration date based on custom duration and time unit.
        """
        if self.time_unit == 'minutes':
            return start_date + timedelta(minutes=self.duration)
        elif self.time_unit == 'hours':
            return start_date + timedelta(hours=self.duration)
        elif self.time_unit == 'days':
            return start_date + timedelta(days=self.duration)
        elif self.time_unit == 'weeks':
            return start_date + timedelta(weeks=self.duration)
        elif self.time_unit == 'months':
            return start_date + relativedelta(months=self.duration)

# Quotation model
class Quotation(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    quotation_id = models.CharField(max_length=6, unique=True, editable=False)  # Unique ID starting with six digits
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Reference to the customer
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)  # Link to SubscriptionPlan
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)  # Amount due for the quotation
    products_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total for additional products
    installation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Installation fee
    due_date = models.DateTimeField()  # Expected due date
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # Quotation status
    created_at = models.DateTimeField(auto_now_add=True)  # When the quotation was created

    def save(self, *args, **kwargs):
        if not self.quotation_id:
            last_quotation = Quotation.objects.all().order_by('id').last()
            if last_quotation:
                new_id = int(last_quotation.quotation_id) + 1
                self.quotation_id = f"{new_id:06d}"
            else:
                self.quotation_id = "000001"
        super(Quotation, self).save(*args, **kwargs)

    def __str__(self):
        return f"Quotation {self.quotation_id} - {self.customer}"

    def calculate_total(self):
        """
        Calculate the total amount due, including subscription price, installation fee, and products.
        """
        items_total = sum(item.item_price for item in self.items.all())  # Sum of all custom items
        return self.amount_due + self.products_total + self.installation_fee + items_total

    def convert_to_invoice(self):
        """
        Convert this quotation into an invoice.
        """
        invoice = Invoice.objects.create(
            customer=self.customer,
            subscription_plan=self.subscription_plan,
            amount_due=self.amount_due,
            products_total=self.products_total,
            installation_fee=self.installation_fee,
            due_date=self.due_date,
            status='Pending',  # Set initial status to Pending
        )
        # Copy over custom items
        for item in self.items.all():
            CustomItem.objects.create(
                invoice=invoice,
                item_name=item.item_name,
                item_description=item.item_description,
                item_price=item.item_price
            )
        return invoice

# Invoice model
class Invoice(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    )

    invoice_id = models.CharField(max_length=6, unique=True, editable=False)  # Unique ID starting with six digits
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Reference to the customer
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)  # Link to SubscriptionPlan
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)  # Amount due for the invoice
    products_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total for additional products
    installation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Installation fee
    due_date = models.DateTimeField()  # Due date of the invoice
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # Invoice status
    penalty_applied = models.BooleanField(default=False)  # Whether penalty is applied for overdue payments
    created_at = models.DateTimeField(auto_now_add=True)  # When the invoice was created

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last_invoice = Invoice.objects.all().order_by('id').last()
            if last_invoice:
                new_id = int(last_invoice.invoice_id) + 1
                self.invoice_id = f"{new_id:06d}"
            else:
                self.invoice_id = "000001"
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_id} - {self.customer}"

    def calculate_total(self):
        """
        Calculate the total amount due, including subscription price, installation fee, products, and custom items.
        """
        items_total = sum(item.item_price for item in self.items.all())  # Sum of all custom items
        return self.amount_due + self.products_total + self.installation_fee + items_total

# Payment model to track payments made towards invoices
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('Mpesa', 'Mpesa'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    )

    payment_id = models.CharField(max_length=6, unique=True, editable=False)  # Unique ID starting with six digits
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)  # Link to the related invoice
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)  # Payment method
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # For Mpesa payments
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    payment_date = models.DateTimeField(auto_now_add=True)  # Date and time of the payment
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Who processed the payment

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
