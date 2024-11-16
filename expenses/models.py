from django.db import models
from django.contrib.auth.models import User
from suppliers.models import Supplier
from django.utils import timezone

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name="subcategories"
    )

    def __str__(self):
        return self.name


class Expense(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit', 'Credit'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Mpesa', 'Mpesa'),
    ]

    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name="expenses")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True,
        help_text="Automatically populated from the supplier if set."
    )
    payment_status = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=255, blank=True, null=True)
    receipt = models.FileField(upload_to='expenses/receipts/', blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_expenses")
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_expenses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically populate payment method from supplier if not manually set
        if self.supplier and not self.payment_method:
            self.payment_method = self.supplier.payment_method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"


class Budget(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name="budgets")
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()
    month = models.IntegerField()

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year} Budget"


class ExpenseLog(models.Model):
    OPERATION_CHOICES = [
        ('CREATE', 'Create'),
        ('READ', 'Read'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, null=True, blank=True, related_name="logs")
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="logs")
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        target = self.expense if self.expense else self.category
        return f"{self.user.username} {self.operation} {target} at {self.timestamp}"
