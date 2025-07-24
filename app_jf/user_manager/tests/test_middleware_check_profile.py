from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse, resolve
from user_manager.middleware.check_profile import ProfileCheck
from user_manager.models import JobSeeker, Agency
from unittest.mock import MagicMock, patch
from datetime import date

# Alors lui il après 1h j'ai laissé l'Ia me le faire, jamais j;aurais pensé a émuler les messages et les redirections
# Enfin si mais TELLEMENT flemme x)
# Rigolo la factory de requete quand meme

class ProfileCheckMiddlewareTests(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Créer les groupes
        self.jobseeker_group = Group.objects.create(name='JobSeeker')
        self.agency_group = Group.objects.create(name='Agency')

        # Créer le middleware avec un mock de get_response
        self.get_response_mock = MagicMock()
        self.get_response_mock.return_value = 'response'
        self.middleware = ProfileCheck(self.get_response_mock)

        # Créer une factory de requêtes
        self.factory = RequestFactory()

    def test_user_without_group_is_redirected_to_select_profile(self):
        """Test qu'un utilisateur sans groupe est redirigé vers select_profile"""
        # Créer une requête vers une page protégée (dashboard)
        request = self.factory.get('/home/dashboard/')
        request.user = self.user

        # Simuler le système de messages
        setattr(request, '_messages', MagicMock())

        # Patch la fonction resolve pour simuler le nom de l'URL
        with patch('user_manager.middleware.check_profile.resolve') as mock_resolve:
            mock_resolve.return_value = MagicMock(url_name='dashboard', namespace='home')

            # Patch la fonction redirect pour capturer la redirection
            with patch('user_manager.middleware.check_profile.redirect') as mock_redirect:
                mock_redirect.return_value = 'redirected'

                # Exécuter le middleware
                response = self.middleware(request)

                # Vérifier que l'utilisateur est redirigé vers select_profile
                mock_redirect.assert_called_once_with('select_profile')
                self.assertEqual(response, 'redirected')

    def test_user_with_jobseeker_group_but_no_profile_is_redirected(self):
        """Test qu'un utilisateur du groupe JobSeeker sans profil est redirigé"""
        # Ajouter l'utilisateur au groupe JobSeeker
        self.user.groups.add(self.jobseeker_group)

        # Créer une requête vers une page protégée
        request = self.factory.get('/home/dashboard/')
        request.user = self.user

        # Simuler le système de messages
        setattr(request, '_messages', MagicMock())

        # Patch la fonction resolve pour simuler le nom de l'URL
        with patch('user_manager.middleware.check_profile.resolve') as mock_resolve:
            mock_resolve.return_value = MagicMock(url_name='dashboard', namespace='home')

            # Patch la fonction redirect pour capturer la redirection
            with patch('user_manager.middleware.check_profile.redirect') as mock_redirect:
                mock_redirect.return_value = 'redirected'

                # Exécuter le middleware
                response = self.middleware(request)

                # Vérifier que l'utilisateur est redirigé vers register_jobseeker
                mock_redirect.assert_called_once_with('register_jobseeker')
                self.assertEqual(response, 'redirected')

    def test_user_with_agency_group_but_no_profile_is_redirected(self):
        """Test qu'un utilisateur du groupe Agency sans profil est redirigé"""
        # Ajouter l'utilisateur au groupe Agency
        self.user.groups.add(self.agency_group)

        # Créer une requête vers une page protégée
        request = self.factory.get('/home/dashboard/')
        request.user = self.user

        # Simuler le système de messages
        setattr(request, '_messages', MagicMock())

        # Patch la fonction resolve pour simuler le nom de l'URL
        with patch('user_manager.middleware.check_profile.resolve') as mock_resolve:
            mock_resolve.return_value = MagicMock(url_name='dashboard', namespace='home')

            # Patch la fonction redirect pour capturer la redirection
            with patch('user_manager.middleware.check_profile.redirect') as mock_redirect:
                mock_redirect.return_value = 'redirected'

                # Exécuter le middleware
                response = self.middleware(request)

                # Vérifier que l'utilisateur est redirigé vers register_agency
                mock_redirect.assert_called_once_with('register_agency')
                self.assertEqual(response, 'redirected')

    def test_user_with_complete_profile_not_redirected(self):
        """Test qu'un utilisateur avec profil complet n'est pas redirigé"""
        # Ajouter l'utilisateur au groupe JobSeeker
        self.user.groups.add(self.jobseeker_group)

        # Créer un profil JobSeeker pour cet utilisateur
        JobSeeker.objects.create(
            user=self.user,
            birthDate=date(1990, 1, 1),
            city="Paris"
        )

        # Créer une requête vers une page protégée
        request = self.factory.get('/home/dashboard/')
        request.user = self.user

        # Simuler le système de messages
        setattr(request, '_messages', MagicMock())

        # Patch la fonction resolve pour simuler le nom de l'URL
        with patch('user_manager.middleware.check_profile.resolve') as mock_resolve:
            mock_resolve.return_value = MagicMock(url_name='dashboard', namespace='home')

            # Exécuter le middleware
            response = self.middleware(request)

            # Vérifier que get_response est appelé (pas de redirection)
            self.get_response_mock.assert_called_once_with(request)
            self.assertEqual(response, 'response')

    def test_excluded_urls_not_checked(self):
        """Test que les URLs exclues ne sont pas vérifiées"""
        # Créer une requête vers une URL exclue (select_profile)
        request = self.factory.get('/user/select-profile/')
        request.user = self.user

        # Simuler le système de messages
        setattr(request, '_messages', MagicMock())

        # Patch la fonction resolve pour simuler le nom de l'URL
        with patch('user_manager.middleware.check_profile.resolve') as mock_resolve:
            mock_resolve.return_value = MagicMock(url_name='select_profile', namespace=None)

            # Exécuter le middleware
            response = self.middleware(request)

            # Vérifier que get_response est appelé (pas de redirection)
            self.get_response_mock.assert_called_once_with(request)
            self.assertEqual(response, 'response')

    def test_anonymous_user_not_checked(self):
        """Test qu'un utilisateur non connecté n'est pas vérifié"""
        # Créer une requête avec un utilisateur anonyme
        request = self.factory.get('/home/dashboard/')
        request.user = MagicMock(is_authenticated=False)

        # Exécuter le middleware
        response = self.middleware(request)
