# Generated by Django 4.2.2 on 2023-06-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deposit", "0003_alter_deposit_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deposit",
            name="amount",
            field=models.DecimalField(decimal_places=10, max_digits=20),
        ),
    ]
