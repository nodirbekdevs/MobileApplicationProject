from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from admin_panel.settings import (
    ENVIRON_DJANGO_SUPERUSER_USERNAME, ENVIRON_DJANGO_SUPERUSER_EMAIL, ENVIRON_DJANGO_SUPERUSER_PASSWORD
)


class Command(BaseCommand):
    help = 'Create a superuser with predefined username and password'

    def handle(self, *args, **options):
        try:
            admin = User.objects.filter(username=ENVIRON_DJANGO_SUPERUSER_USERNAME).exists()

            if admin:
                print('Superuser already exists')
                return

            User.objects.create_superuser(
                username=ENVIRON_DJANGO_SUPERUSER_USERNAME,
                email=ENVIRON_DJANGO_SUPERUSER_EMAIL,
                password=ENVIRON_DJANGO_SUPERUSER_PASSWORD
            )

            print('Superuser created successfully')

        except Exception as error:
            print(error)
