from django.db import models

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name="expenses")
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=(('Cash', 'Cash'), ('Credit', 'Credit'), ('Bank Transfer', 'Bank Transfer')))
    supplier = models.CharField(max_length=100, blank=True, null=True)
    receipt = models.FileField(upload_to='expenses/receipts/', blank=True, null=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"

