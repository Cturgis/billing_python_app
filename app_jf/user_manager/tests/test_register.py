from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class RegisterTests(TestCase):
    """Tests pour la vue d'inscription"""

    def setUp(self):
        # Créer les groupes nécessaires pour les tests
        self.jobseeker_group, _ = Group.objects.get_or_create(name='JobSeeker')
        self.agency_group, _ = Group.objects.get_or_create(name='Agency')

    def test_register_view_uses_correct_template(self):
        """Test que la vue d'inscription utilise le bon template"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_manager/register.html')

    def test_register_form_contains_expected_fields(self):
        """Test que le formulaire d'inscription contient les champs attendus"""
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'name="confirm_password"')

    def test_register_login_link_exists(self):
        """Test que le lien vers la page de connexion existe"""
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'Vous avez déjà un compte ?')
        self.assertContains(response, f'<a href="{reverse("login")}">Connectez-vous</a>')

    def test_successful_registration_creates_user(self):
        """Test qu'une inscription réussie crée un utilisateur"""
        user_count = get_user_model().objects.count()

        response = self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        }, follow=True)

        # Vérifier qu'un nouvel utilisateur a été créé
        self.assertEqual(get_user_model().objects.count(), user_count + 1)

        # Vérifier que l'utilisateur a été créé avec les bons attributs
        user = get_user_model().objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')

    def test_password_mismatch_shows_error(self):
        """Test qu'une erreur est affichée si les mots de passe ne correspondent pas"""
        response = self.client.post(reverse('register'), {
            'email': 'mismatch@example.com',
            'username': 'mismatch',
            'first_name': 'Mismatch',
            'last_name': 'User',
            'password': 'password123',
            'confirm_password': 'differentpassword',
        })

        self.assertContains(response, 'Les mots de passe ne correspondent pas')

    def test_duplicate_email_shows_error(self):
        """Test qu'une erreur est affichée si l'email existe déjà"""
        # Créer un utilisateur avec l'email test
        User = get_user_model()
        User.objects.create_user(
            username='existinguser',
            email='duplicate@example.com',
            password='testpass123'
        )

        # Tenter de créer un nouvel utilisateur avec le même email
        response = self.client.post(reverse('register'), {
            'email': 'duplicate@example.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        })

        self.assertContains(response, 'Un utilisateur avec cette adresse e-mail existe')

    def test_duplicate_username_shows_error(self):
        """Test qu'une erreur est affichée si le nom d'utilisateur existe déjà"""
        User = get_user_model()
        User.objects.create_user(
            username='duplicateuser',
            email='original@example.com',
            password='testpass123'
        )

        # Tenter de créer un nouvel utilisateur avec le même username
        response = self.client.post(reverse('register'), {
            'email': 'new@example.com',
            'username': 'duplicateuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        })

        self.assertContains(response, 'Un utilisateur avec ce nom d&#x27;utilisateur existe')

    def test_successful_registration_redirects_to_select_profile(self):
        """Test qu'après une inscription réussie, l'utilisateur est redirigé vers la sélection de profil"""
        response = self.client.post(reverse('register'), {
            'email': 'redirect@example.com',
            'username': 'redirectuser',
            'first_name': 'Redirect',
            'last_name': 'User',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        }, follow=True)

        self.assertRedirects(response, reverse('select_profile'))

    def test_successful_registration_logs_in_user(self):
        """Test qu'après une inscription réussie, l'utilisateur est automatiquement connecté"""
        self.client.post(reverse('register'), {
            'email': 'autologin@example.com',
            'username': 'autologinuser',
            'first_name': 'Auto',
            'last_name': 'Login',
            'password': 'securepass123',
            'confirm_password': 'securepass123',
        }, follow=True)

        # Vérifier que l'utilisateur est connecté
        response = self.client.get(reverse('select_profile'))
        self.assertEqual(response.status_code, 200)  # Si l'utilisateur n'était pas connecté, ce serait un 302
