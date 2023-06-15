# Generated by Django 4.2.2 on 2023-06-15 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="wallet",
            name="balance",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
