from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user_manager.models import Agency

class RegisterAgencyTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'birthDate': '1990-01-01',
            'city': 'Paris',
        }

    def test_register_agency_success(self):
        # Register a new user (jobseeker)
        self.client.post(reverse('register'), self.user_data, follow=True)
        self.client.login(username='testuser', password='testpassword123')
        # Register agency
        agency_data = {
            'name': 'Test Agency',
            'address': '123 Rue de Test',
            'siret': '12345678901234',
        }
        response = self.client.post(reverse('register_agency'), agency_data, follow=True)
        user = get_user_model().objects.get(username='testuser')
        self.assertTrue(hasattr(user, 'agency_profile'))
        agency = user.agency_profile
        self.assertEqual(agency.name, 'Test Agency')
        self.assertEqual(agency.address, '123 Rue de Test')
        self.assertEqual(agency.siret, '12345678901234')
        self.assertContains(response, 'Agence créée et associée à votre compte.')

    def test_register_agency_skip(self):
        # Register a new user (jobseeker)
        self.client.post(reverse('register'), self.user_data, follow=True)
        self.client.login(username='testuser', password='testpassword123')
        # Skip agency registration
        response = self.client.post(reverse('register_agency'), {'skip': '1'}, follow=True)
        user = get_user_model().objects.get(username='testuser')
        self.assertFalse(hasattr(user, 'agency_profile'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_register_agency_duplicate_siret(self):
        # Register a first user and agency
        self.client.post(reverse('register'), self.user_data, follow=True)
        self.client.login(username='testuser', password='testpassword123')
        agency_data = {
            'name': 'Test Agency',
            'address': '123 Rue de Test',
            'siret': '12345678901234',
        }
        self.client.post(reverse('register_agency'), agency_data, follow=True)
        # Register a second user
        user2_data = self.user_data.copy()
        user2_data['username'] = 'testuser2'
        user2_data['email'] = 'testuser2@example.com'
        self.client.post(reverse('register'), user2_data, follow=True)
        self.client.login(username='testuser2', password='testpassword123')
        # Try to register agency with same siret
        response = self.client.post(reverse('register_agency'), agency_data, follow=True)
        self.assertFormError(response.context['form'], 'siret', 'Agency with this Siret already exists.')

