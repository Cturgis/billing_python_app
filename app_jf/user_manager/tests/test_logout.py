from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from user_manager.models import Agency


class LogoutViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.admin = User.objects.create_user(username='admin', password='adminpassword')
        self.admin.groups.add(self.admin_group)

    def test_logout_redirects_to_login(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('login'))
        # Vérifie que l'utilisateur est bien déconnecté
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout_when_not_logged_in(self):
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('login'))
