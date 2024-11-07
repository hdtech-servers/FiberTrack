# Generated by Django 5.1.2 on 2024-11-05 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
        ('services', '0002_rename_bandwidth_subscriptionplan_download_speed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='subscription_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.subscriptionplan'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='subscription_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.subscriptionplan'),
        ),
        migrations.DeleteModel(
            name='SubscriptionPlan',
        ),
    ]