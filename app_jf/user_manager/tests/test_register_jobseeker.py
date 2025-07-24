from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from user_manager.models import JobSeeker

class RegisterJobSeekerTests(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name='JobSeeker')

    def test_register_jobseeker_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123',
            'first_name': 'Jean',
            'last_name': 'Test',
            'birthDate': '1995-05-10',
            'city': 'Paris',
        }, follow=True)
        User = get_user_model()
        user = User.objects.get(username='newuser')
        self.assertTrue(user.groups.filter(name='JobSeeker').exists())
        self.assertTrue(hasattr(user, 'jobseeker_profile'))
        self.assertEqual(user.jobseeker_profile.birthDate.strftime('%Y-%m-%d'), '1995-05-10')
        self.assertEqual(user.jobseeker_profile.city, 'Paris')
        self.assertContains(response, 'Inscription réussie')

    def test_register_jobseeker_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password': 'testpassword123',
            'confirm_password': 'wrongpassword',
            'first_name': 'Marie',
            'last_name': 'Test',
            'birthDate': '1990-01-01',
            'city': 'Lyon',
        })
        self.assertFormError(response.context['form'], 'confirm_password', 'Les mots de passe ne correspondent pas.')
        User = get_user_model()
        self.assertFalse(User.objects.filter(username='newuser2').exists())

    def test_register_jobseeker_missing_field(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': 'nouser@example.com',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123',
            'first_name': 'No',
            'last_name': 'Name',
            'birthDate': '2000-01-01',
            'city': 'Marseille',
        })
        self.assertFormError(response.context['form'], 'username', 'This field is required.')

    def test_register_jobseeker_duplicate_username(self):
        User = get_user_model()
        User.objects.create_user(username='dupuser', email='dup@example.com', password='dup12345')
        response = self.client.post(reverse('register'), {
            'username': 'dupuser',
            'email': 'dup2@example.com',
            'password': 'dup12345',
            'confirm_password': 'dup12345',
            'first_name': 'Dup',
            'last_name': 'User',
            'birthDate': '1999-09-09',
            'city': 'Nice',
        })
        self.assertFormError(response.context['form'], 'username', 'A user with that username already exists.')

    def test_register_jobseeker_duplicate_email(self):
        User = get_user_model()
        User.objects.create_user(username='uniqueuser', email='dupemail@example.com', password='dup12345')
        response = self.client.post(reverse('register'), {
            'username': 'anotheruser',
            'email': 'dupemail@example.com',
            'password': 'dup12345',
            'confirm_password': 'dup12345',
            'first_name': 'Dup',
            'last_name': 'Email',
            'birthDate': '1999-09-09',
            'city': 'Nice',
        })
        self.assertFormError(response.context['form'], 'email', 'Un utilisateur avec cette adresse e-mail existe déjà.')
