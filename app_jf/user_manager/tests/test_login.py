from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from user_manager.models import Agency

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
        # Crée une agence
        self.agency = User.objects.create_user(username='agency', password='agencypassword', first_name='Entreprise', last_name='Demo')
        self.agency.groups.add(self.agency_group)
        Agency.objects.create(user=self.agency, name='Agence Démo', address='1 rue de l’Emploi, Paris', siret='12345678901234')

    def test_login_admin(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'adminpassword'}, follow=True)
        self.assertContains(response, 'Connexion réussie en tant que Admin')

    def test_login_jobseeker(self):
        response = self.client.post(reverse('login'), {'username': 'jobseeker', 'password': 'jobseekerpassword'}, follow=True)
        self.assertContains(response, 'Connexion réussie en tant que JobSeeker')

    def test_login_agency(self):
        response = self.client.post(reverse('login'), {'username': 'agency', 'password': 'agencypassword'}, follow=True)
        self.assertContains(response, 'Connexion réussie en tant que Agency')

    def test_login_wrong_password(self):
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'wrongpass'}, follow=True)
        self.assertContains(response, 'Nom d&#x27;utilisateur ou mot de passe incorrect')

    def test_login_wrong_username(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'adminpassword'}, follow=True)
        self.assertContains(response, 'Nom d&#x27;utilisateur ou mot de passe incorrect')

