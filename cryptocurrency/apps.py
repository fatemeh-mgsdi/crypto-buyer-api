from django.apps import AppConfig


class CryptocurrencyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cryptocurrency"

    def ready(self):
        import cryptocurrency.signals
