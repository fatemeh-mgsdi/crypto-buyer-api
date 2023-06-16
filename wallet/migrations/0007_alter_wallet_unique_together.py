# Generated by Django 4.2.2 on 2023-06-16 12:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cryptocurrency", "0002_alter_cryptocurrency_past24"),
        ("wallet", "0006_alter_wallet_user"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="wallet",
            unique_together={("user", "crypto")},
        ),
    ]
