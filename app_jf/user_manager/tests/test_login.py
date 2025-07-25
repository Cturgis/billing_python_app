from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from user_manager.models import Agency, JobSeeker
from datetime import date

class LoginViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        # Crée les groupes
        self.admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.agency_group, _ = Group.objects.get_or_create(name='Agency')
        self.jobseeker_group, _ = Group.objects.get_or_create(name='JobSeeker')
        # Crée un admin
        self.admin = User.objects.create_user(username='admin', password='adminpassword', first_name='Admin', last_name='User')
        self.admin.groups.add(self.admin_group)

        # Crée un jobseeker
        self.jobseeker = User.objects.create_user(username='jobseeker', password='jobseekerpassword', first_name='Jean', last_name='Chercheur')
        self.jobseeker.groups.add(self.jobseeker_group)
        JobSeeker.objects.create(user=self.jobseeker, birthDate=date(1990, 1, 1), city='Paris')

        # Crée une agence
        self.agency = User.objects.create_user(username='agency', password='agencypassword', first_name='Entreprise', last_name='Demo')
        self.agency.groups.add(self.agency_group)
        Agency.objects.create(user=self.agency, name='Agence Démo', address='1 rue de l\'Emploi, Paris', siret='12345678901234')

    def test_login_admin(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'adminpassword'}, follow=True)
        self.assertRedirects(response, reverse('job_finder:dashboard'))

    def test_login_jobseeker(self):
        response = self.client.post(reverse('login'), {'username': 'jobseeker', 'password': 'jobseekerpassword'}, follow=True)
        self.assertRedirects(response, reverse('job_finder:dashboard'))

    def test_login_agency(self):
        response = self.client.post(reverse('login'), {'username': 'agency', 'password': 'agencypassword'}, follow=True)
        self.assertRedirects(response, reverse('job_finder:dashboard'))

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Reste sur la page de login
        self.assertContains(response, 'utilisateur ou mot de passe incorrect')

    def test_login_remember_username(self):
        """Vérifie que le nom d'utilisateur est conservé après une erreur de connexion"""
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertContains(response, 'value="testuser"')

    def test_login_page_has_register_link(self):
        """Vérifie que la page de login contient un lien vers la page d'inscription"""
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'pas encore de compte')
        self.assertContains(response, reverse('register'))
