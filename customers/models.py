from django.db import models
import random
import string

class Customer(models.Model):
    customer_id = models.CharField(max_length=20, unique=True, blank=True)  # Auto-generated field
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pppoe_username = models.CharField(max_length=50, blank=True)  # Auto-generated, same as customer_id
    pppoe_password = models.CharField(max_length=50, blank=True)  # Randomly generated password
    billing_address = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            last_customer = Customer.objects.all().order_by('id').last()
            if last_customer:
                customer_id_number = int(last_customer.customer_id[3:]) + 1
            else:
                customer_id_number = 1
            self.customer_id = 'OPT' + str(customer_id_number).zfill(6)  # e.g., OPT000001

        # Assign PPPoE username same as Customer ID
        if not self.pppoe_username:
            self.pppoe_username = self.customer_id

        # Auto-generate PPPoE password if not provided
        if not self.pppoe_password:
            self.pppoe_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
