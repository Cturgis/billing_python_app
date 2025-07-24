from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create default admin and customer users if they do not exist, and assign them to groups.'

    def handle(self, *args, **options):
        User = get_user_model()
        # Ensure groups exist
        admin_group, _ = Group.objects.get_or_create(name='admin')
        customer_group, _ = Group.objects.get_or_create(name='customer')
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('Created admin user and added to admin group'))
        else:
            admin_user = User.objects.get(username='admin')
            admin_user.groups.add(admin_group)
            self.stdout.write('Admin user already exists, added to admin group')
        # Create customer user
        if not User.objects.filter(username='customer').exists():
            customer_user = User.objects.create_user('customer', 'customer@example.com', 'customerpassword')
            customer_user.groups.add(customer_group)
            self.stdout.write(self.style.SUCCESS('Created customer user and added to customer group'))
        else:
            customer_user = User.objects.get(username='customer')
            customer_user.groups.add(customer_group)
            self.stdout.write('Customer user already exists, added to customer group')
