from django.db import models
import random
import string

class Customer(models.Model):
    customer_id = models.CharField(max_length=20, unique=True, blank=True)  # Auto-generated field
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pppoe_username = models.CharField(max_length=50, blank=True)  # Can be autogenerated or manually adjusted
    pppoe_password = models.CharField(max_length=50, blank=True)  # Can be autogenerated or manually adjusted
    billing_address = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # Account fields
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Auto-generate a unique customer_id if not provided
        if not self.customer_id:
            last_customer = Customer.objects.exclude(customer_id="").order_by('id').last()
            if last_customer and last_customer.customer_id.startswith('OPT'):
                # Increment the last numerical part of customer_id
                customer_id_number = int(last_customer.customer_id[3:]) + 1
            else:
                customer_id_number = 1
            self.customer_id = 'OPT' + str(customer_id_number).zfill(6)  # e.g., OPT000001

        # Autogenerate PPPoE username if blank, or use customer_id
        if not self.pppoe_username:
            self.pppoe_username = self.customer_id

        # Autogenerate PPPoE password if blank
        if not self.pppoe_password:
            self.pppoe_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Update credit and outstanding amounts based on account balance
        if self.account_balance >= 0:
            self.credit = self.account_balance
            self.outstanding_amount = 0
        else:
            self.credit = 0
            self.outstanding_amount = abs(self.account_balance)

        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
