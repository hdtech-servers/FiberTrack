# Generated by Django 5.1.2 on 2024-11-09 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(blank=True, editable=False, max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='quotation_id',
            field=models.CharField(blank=True, editable=False, max_length=20, unique=True),
        ),
    ]
