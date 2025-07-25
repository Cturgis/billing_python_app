from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from user_manager.models.JobSeeker import JobSeeker
from user_manager.models.Agency import Agency

class DashboardViewTests(TestCase):
    def setUp(self):
        # Créer les groupes
        self.admin_group = Group.objects.create(name='Admin')
        self.agency_group = Group.objects.create(name='Agency')
        self.jobseeker_group = Group.objects.create(name='JobSeeker')

        # Créer un utilisateur admin
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='adminpassword'
        )
        self.admin_user.groups.add(self.admin_group)

        # Créer un utilisateur d'agence
        self.agency_user = User.objects.create_user(
            username='agency_test',
            email='agency@test.com',
            password='agencypassword'
        )
        self.agency_user.groups.add(self.agency_group)
        # Créer une agence associée à cet utilisateur
        self.agency = Agency.objects.create(
            user=self.agency_user,
            name="Test Agency",
            address="123 Test Street",
            siret="12345678901234"
        )

        # Créer un demandeur d'emploi
        self.jobseeker_user = User.objects.create_user(
            username='jobseeker_test',
            email='jobseeker@test.com',
            password='jobseekerpassword'
        )
        self.jobseeker_user.groups.add(self.jobseeker_group)
        # Créer un profil jobseeker associé
        self.jobseeker = JobSeeker.objects.create(
            user=self.jobseeker_user,
            city="Paris",
            birthDate="1990-01-01"
        )

        self.client = Client()

    def test_dashboard_access_not_logged_in(self):
        """Test qu'un utilisateur non connecté est redirigé vers la page de connexion"""
        response = self.client.get(reverse('job_finder:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertIn('/user/login/', response.url)

    def test_dashboard_access_admin(self):
        """Test qu'un admin peut accéder au dashboard et voit les éléments appropriés"""
        self.client.login(username='admin_test', password='adminpassword')
        response = self.client.get(reverse('job_finder:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin_test')
        self.assertContains(response, 'Admin')  # Vérifier avec la casse correcte

        # Vérifier que les liens spécifiques aux admins sont présents
        self.assertContains(response, 'Utilisateurs')
        self.assertContains(response, 'Rapports')

    def test_dashboard_access_agency(self):
        """Test qu'une agence peut accéder au dashboard et voit les éléments appropriés"""
        self.client.login(username='agency_test', password='agencypassword')
        response = self.client.get(reverse('job_finder:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'agency_test')
        self.assertContains(response, 'Agency')  # Vérifier avec la casse correcte

        # Vérifier que les liens spécifiques aux agences sont présents
        self.assertContains(response, 'Mes offres')
        self.assertContains(response, 'Publier une offre')
        self.assertContains(response, 'Candidatures reçues')

    def test_dashboard_access_jobseeker(self):
        """Test qu'un chercheur d'emploi peut accéder au dashboard et voit les éléments appropriés"""
        self.client.login(username='jobseeker_test', password='jobseekerpassword')
        response = self.client.get(reverse('job_finder:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'jobseeker_test')
        self.assertContains(response, 'JobSeeker')  # Vérifier avec la casse correcte

        # Vérifier que les liens spécifiques aux chercheurs d'emploi sont présents
        self.assertContains(response, 'Rechercher des offres')
        self.assertContains(response, 'Mes candidatures')
        self.assertContains(response, 'Mes documents')
