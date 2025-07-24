from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from user_manager.models import JobSeeker
from datetime import date


class RegisterJobSeekerTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.test_user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.jobseeker_group, _ = Group.objects.get_or_create(name='JobSeeker')

    def test_redirect_if_not_logged_in(self):
        """Test que les utilisateurs non connectés sont redirigés vers la page de connexion"""
        response = self.client.get(reverse('register_jobseeker'))
        self.assertRedirects(
            response,
            f'/user/login/?next={reverse("register_jobseeker")}',
            status_code=302,
            target_status_code=200
        )

    def test_view_url_accessible_by_name(self):
        """Test que l'URL est accessible par son nom"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('register_jobseeker'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test que la vue utilise le bon template"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('register_jobseeker'))
        self.assertTemplateUsed(response, 'user_manager/register_jobseeker.html')

    def test_form_contains_expected_fields(self):
        """Test que le formulaire contient les champs attendus"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('register_jobseeker'))
        self.assertContains(response, 'name="birthDate"')
        self.assertContains(response, 'name="city"')

    def test_successful_form_submission_creates_jobseeker_profile(self):
        """Test qu'une soumission réussie crée un profil JobSeeker"""
        self.client.login(username='testuser', password='testpassword')
        self.assertEqual(JobSeeker.objects.count(), 0)
        response = self.client.post(reverse('register_jobseeker'), {
            'birthDate': '1990-01-01',
            'city': 'Paris'
        }, follow=True)
        self.assertEqual(JobSeeker.objects.count(), 1)
        jobseeker = JobSeeker.objects.first()
        self.assertEqual(jobseeker.user, self.test_user)
        self.assertEqual(jobseeker.birthDate, date(1990, 1, 1))
        self.assertEqual(jobseeker.city, 'Paris')

    def test_successful_form_adds_user_to_jobseeker_group(self):
        """Test qu'une soumission réussie ajoute l'utilisateur au groupe JobSeeker"""
        self.client.login(username='testuser', password='testpassword')
        self.assertFalse(self.test_user.groups.filter(name='JobSeeker').exists())
        response = self.client.post(reverse('register_jobseeker'), {
            'birthDate': '1990-01-01',
            'city': 'Paris'
        }, follow=True)
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.groups.filter(name='JobSeeker').exists())

    def test_successful_form_redirects_to_dashboard(self):
        """Test qu'une soumission réussie redirige vers le tableau de bord"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('register_jobseeker'), {
            'birthDate': '1990-01-01',
            'city': 'Paris'
        }, follow=True)
        self.assertRedirects(response, reverse('job_finder:dashboard'))

    def test_invalid_form_shows_error(self):
        """Test qu'un formulaire invalide affiche des erreurs"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('register_jobseeker'), {
            'city': 'Paris'
        })
        self.assertEqual(JobSeeker.objects.count(), 0)
        self.assertContains(response, 'Ce champ est obligatoire')
