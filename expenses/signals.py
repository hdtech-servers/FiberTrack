from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Expense, ExpenseCategory, ExpenseLog

@receiver(post_save, sender=Expense)
def log_expense_operations(sender, instance, created, **kwargs):
    user = instance.last_updated_by if not created else instance.created_by
    operation = 'CREATE' if created else 'UPDATE'
    ExpenseLog.objects.create(
        user=user,
        operation=operation,
        expense=instance,
        description=f"{operation} operation on Expense ID: {instance.id}"
    )

@receiver(post_delete, sender=Expense)
def log_expense_deletion(sender, instance, **kwargs):
    ExpenseLog.objects.create(
        user=instance.last_updated_by,
        operation='DELETE',
        expense=instance,
        description=f"DELETE operation on Expense ID: {instance.id}"
    )

@receiver(post_save, sender=ExpenseCategory)
def log_category_operations(sender, instance, created, **kwargs):
    operation = 'CREATE' if created else 'UPDATE'
    ExpenseLog.objects.create(
        user=None,  # Optional: Associate a user if available
        operation=operation,
        category=instance,
        description=f"{operation} operation on Category ID: {instance.id}"
    )

@receiver(post_delete, sender=ExpenseCategory)
def log_category_deletion(sender, instance, **kwargs):
    ExpenseLog.objects.create(
        user=None,
        operation='DELETE',
        category=instance,
        description=f"DELETE operation on Category ID: {instance.id}"
    )
