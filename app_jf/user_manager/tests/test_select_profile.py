from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class SelectProfileTypeTests(TestCase):
    def setUp(self):
        # Créer un utilisateur pour les tests
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_redirect_if_not_logged_in(self):
        """Test que les utilisateurs non connectés sont redirigés vers la page de connexion"""
        response = self.client.get(reverse('select_profile'))
        self.assertRedirects(
            response,
            f'/user/login/?next={reverse("select_profile")}',
            status_code=302,
            target_status_code=200
        )

    def test_view_url_accessible_by_logged_in_user(self):
        """Test que la page est accessible pour un utilisateur connecté"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('select_profile'))
        self.assertEqual(response.status_code, 200)

    def test_form_contains_expected_choices(self):
        """Test que le formulaire contient les choix attendus"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('select_profile'))
        self.assertContains(response, 'Je suis un particulier')
        self.assertContains(response, 'Je suis une entreprise')

    def test_redirect_to_jobseeker_profile_form(self):
        """Test que la sélection de 'jobseeker' redirige vers le formulaire approprié"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('select_profile'),
            {'profile_type': 'jobseeker'},
            follow=True
        )
        self.assertRedirects(response, reverse('register_jobseeker'))
        # Vérifier que le type de profil est stocké en session
        self.assertEqual(self.client.session['profile_type'], 'jobseeker')

    def test_redirect_to_agency_profile_form(self):
        """Test que la sélection de 'agency' redirige vers le formulaire approprié"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('select_profile'),
            {'profile_type': 'agency'},
            follow=True
        )
        self.assertRedirects(response, reverse('register_agency'))
        self.assertEqual(self.client.session['profile_type'], 'agency')
