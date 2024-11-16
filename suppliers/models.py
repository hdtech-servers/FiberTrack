from django.db import models

class Supplier(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Paybill', 'Paybill'),
        ('Till', 'Till (Buy Goods)'),
        ('Phone', 'Phone Number'),
    ]

    supplier_id = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Payment details fields
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    paybill_number = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    till_number = models.CharField(max_length=20, blank=True, null=True)
    phone_payment_number = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-generate supplier ID if not set
        if not self.supplier_id:
            max_id = Supplier.objects.aggregate(max_id=models.Max('id'))['max_id']
            new_id = max_id + 1 if max_id else 1
            self.supplier_id = f'SP{new_id:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
