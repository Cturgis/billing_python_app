import unittest
from django.test import TestCase
from django.contrib.auth.models import User, Group
from billing.models.Customer import Customer


class UserCreationTestCase(TestCase):
    def test_create_admin_user(self):
        admin_group, _ = Group.objects.get_or_create(name='admin')
        user = User.objects.create_user(username='adminuser', email='admin@example.com', password='adminpass')
        user.groups.add(admin_group)
        self.assertTrue(user.groups.filter(name='admin').exists())
        self.assertEqual(user.username, 'adminuser')
        self.assertEqual(user.email, 'admin@example.com')

    def test_create_customer_user(self):
        customer_group, _ = Group.objects.get_or_create(name='customer')
        user = User.objects.create_user(username='customeruser', email='customer@example.com', password='customerpass')
        user.groups.add(customer_group)
        customer = Customer.objects.create(user=user, address='123 rue de Paris')
        self.assertTrue(user.groups.filter(name='customer').exists())
        self.assertEqual(customer.user.username, 'customeruser')
        self.assertEqual(customer.address, '123 rue de Paris')


if __name__ == '__main__':
    unittest.main()
