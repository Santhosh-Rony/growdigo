from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='growdigoadmin',
                email='admin@growdigo.com',
                password='growdigo@123'
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created superuser: growdigo_admin')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser already exists')
            ) 