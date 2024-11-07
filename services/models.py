# services/models.py

from django.db import models
from datetime import timedelta, datetime, time
from dateutil.relativedelta import relativedelta


class SubscriptionPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('pppoe', 'PPPoE'),
        ('hotspot', 'Hotspot'),
    ]
    TIME_UNIT_CHOICES = [
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ]

    name = models.CharField(max_length=100)  # Plan Name
    upload_speed = models.CharField(max_length=50)
    download_speed = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price
    installation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Installation fee
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPE_CHOICES, default='pppoe')  # Type of the plan
    duration = models.PositiveIntegerField()  # Duration of the plan
    time_unit = models.CharField(max_length=10, choices=TIME_UNIT_CHOICES, default='days')  # Time unit for duration
    data_cap = models.CharField(max_length=50, null=True, blank=True)  # Optional data cap for the plan

    def __str__(self):
        return f"{self.name} - {self.upload_speed}/{self.download_speed} @ {self.price} for {self.duration} {self.time_unit}"

    def get_expiration_date(self, start_date):
        """Calculate expiration date based on duration and time unit."""
        if self.time_unit == 'minutes':
            return start_date + timedelta(minutes=self.duration)
        elif self.time_unit == 'hours':
            return start_date + timedelta(hours=self.duration)
        elif self.time_unit == 'days':
            return start_date + timedelta(days=self.duration)
        elif self.time_unit == 'weeks':
            return start_date + timedelta(weeks=self.duration)
        elif self.time_unit == 'months':
            # Add months and set time to midnight on the expiration day
            expiration_date = start_date + relativedelta(months=self.duration)
            return datetime.combine(expiration_date.date(), time.min)  # Sets time to 00:00:00
