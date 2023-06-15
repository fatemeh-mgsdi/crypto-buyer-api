from django.core.management.base import BaseCommand
from user.models import User
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        admin = settings.ADMIN_CREDENTIALS
        if not User.objects.filter(email=admin['email']).exists():
            User.objects.create_superuser(email=admin['email'], first_name=admin['first_name'], last_name=admin['last_name'], password=admin['password'])

    