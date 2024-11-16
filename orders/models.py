from django.core.exceptions import ValidationError
from django.db import models
from suppliers.models import Supplier
from inventory.models import Product

class Order(models.Model):
    # Fields for Order Model
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Payment options for the order
    PAYMENT_OPTIONS = [
        ('pay_now', 'Pay Now'),
        ('pay_on_delivery', 'Pay on Delivery'),
    ]
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTIONS, default='pay_on_delivery')

    # Payment status based on payment progress
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid', editable=False)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically generate an order number if it's not set
        if not self.order_number:
            max_id = Order.objects.aggregate(max_id=models.Max('id'))['max_id']
            new_id = max_id + 1 if max_id else 1
            self.order_number = f'ORD{new_id:06d}'

        # Calculate total amount from OrderItems
        self.total_amount = sum(item.quantity_ordered * item.buying_price for item in self.items.all())

        # Set payment status based on payment option and paid amount
        if self.payment_option == 'pay_now':
            self.payment_status = 'paid' if self.paid_amount >= self.total_amount else 'unpaid'
        elif self.payment_option == 'pay_on_delivery':
            if self.paid_amount == 0:
                self.payment_status = 'unpaid'
            elif self.paid_amount < self.total_amount:
                self.payment_status = 'partially_paid'
            elif self.paid_amount >= self.total_amount:
                self.payment_status = 'paid'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    def update_payment(self, amount):
        """Method to update paid amount and adjust payment status."""
        self.paid_amount += amount
        self.save()  # Re-save to update payment_status based on new paid_amount


class OrderItem(models.Model):
    # Fields for OrderItem Model
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    quantity_delivered = models.PositiveIntegerField(default=0)  # Track delivered quantity
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity_ordered})"

    def clean(self):
        """Ensure quantity_delivered does not exceed quantity_ordered."""
        if self.quantity_delivered > self.quantity_ordered:
            raise ValidationError("Delivered quantity cannot exceed ordered quantity.")
