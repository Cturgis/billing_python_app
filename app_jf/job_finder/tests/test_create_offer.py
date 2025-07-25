from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from job_finder.models.JobOffer import JobOffer
from user_manager.models.Agency import Agency
from decimal import Decimal
from django.contrib.messages import get_messages

class CreateOfferTests(TestCase):
    def setUp(self):
        # Créer le groupe Agency
        self.agency_group = Group.objects.create(name='Agency')

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

        # URL pour la création d'offre
        self.create_url = reverse('job_finder:create_offer')

        # Client authentifié en tant qu'agence
        self.client = Client()
        self.client.login(username='agency_test', password='agencypassword')

        # Données de formulaire valides par défaut
        self.valid_form_data = {
            'title': 'Développeur Python Senior',
            'contract_type': 'CDI',
            'experience_required': 'SENIOR',
            'description': 'Nous recherchons un développeur Python expérimenté pour rejoindre notre équipe.',
        }

    def test_create_offer_page_access(self):
        """Test que la page de création d'offre est accessible pour les utilisateurs du groupe Agency"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_finder/agency/create_offer.html')

    def test_create_offer_page_access_unauthorized(self):
        """Test que la page est inaccessible pour les utilisateurs non Agency"""
        # Créer un utilisateur non-agency
        user = User.objects.create_user(
            username='regular_user',
            email='user@test.com',
            password='userpassword'
        )

        # Connecter cet utilisateur
        self.client.logout()
        self.client.login(username='regular_user', password='userpassword')

        # Essayer d'accéder à la page
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)  # Redirection attendue

        # Vérifier le message d'erreur
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Veuillez d'abord choisir votre type de profil.", str(messages[0]))

    def test_create_valid_offer(self):
        """Test la création d'une offre valide avec les champs minimums requis"""
        # Nombre d'offres avant
        offer_count_before = JobOffer.objects.count()

        # Soumettre le formulaire
        response = self.client.post(self.create_url, self.valid_form_data, follow=True)

        # Vérifier la redirection
        self.assertRedirects(response, reverse('job_finder:agency_offers'))

        # Vérifier qu'une nouvelle offre a été créée
        self.assertEqual(JobOffer.objects.count(), offer_count_before + 1)

        # Récupérer l'offre créée
        offer = JobOffer.objects.latest('publication_date')

        # Vérifier les champs
        self.assertEqual(offer.title, self.valid_form_data['title'])
        self.assertEqual(offer.contract_type, self.valid_form_data['contract_type'])
        self.assertEqual(offer.experience_required, self.valid_form_data['experience_required'])
        self.assertEqual(offer.description, self.valid_form_data['description'])
        self.assertEqual(offer.agency, self.agency)
        self.assertTrue(offer.is_active)

        # Vérifier que la référence a été générée automatiquement
        self.assertTrue(offer.reference.startswith('JF-'))

    def test_create_offer_with_all_fields(self):
        """Test la création d'une offre avec tous les champs remplis"""
        # Préparer les données avec tous les champs
        full_data = self.valid_form_data.copy()
        full_data.update({
            'contract_type': 'CDD',
            'contract_duration': 6,
            'min_salary': 40000,
            'max_salary': 50000,
            'location': 'Paris, France'
        })

        # Soumettre le formulaire
        response = self.client.post(self.create_url, full_data, follow=True)

        # Vérifier la redirection
        self.assertRedirects(response, reverse('job_finder:agency_offers'))

        # Récupérer l'offre créée
        offer = JobOffer.objects.latest('publication_date')

        # Vérifier les champs supplémentaires
        self.assertEqual(offer.contract_type, 'CDD')
        self.assertEqual(offer.contract_duration, 6)
        self.assertEqual(offer.min_salary, Decimal('40000'))
        self.assertEqual(offer.max_salary, Decimal('50000'))
        self.assertEqual(offer.location, 'Paris, France')

        # Vérifier le formatage de la fourchette de salaire
        self.assertEqual(offer.salary_range, 'De 40000.00 € à 50000.00 €')

    def test_create_offer_missing_required_fields(self):
        """Test que le formulaire est invalide si des champs requis sont manquants"""
        # Données incomplètes (titre manquant)
        incomplete_data = self.valid_form_data.copy()
        del incomplete_data['title']

        # Soumettre le formulaire
        response = self.client.post(self.create_url, incomplete_data)

        # Vérifier que la page est rechargée avec une erreur
        self.assertEqual(response.status_code, 200)

        # Vérifier que le message d'erreur est bien présent dans le contenu de la page
        self.assertContains(response, "This field is required.")

        # Vérifier qu'aucune offre n'a été créée avec ces données
        self.assertFalse(JobOffer.objects.filter(contract_type=incomplete_data['contract_type'],
                                               experience_required=incomplete_data['experience_required']).exists())

    def test_cdd_without_duration(self):
        """Test que le formulaire est invalide si un CDD est sélectionné sans durée"""
        # Données avec CDD mais sans durée
        cdd_data = self.valid_form_data.copy()
        cdd_data['contract_type'] = 'CDD'

        # Soumettre le formulaire
        response = self.client.post(self.create_url, cdd_data)

        # Vérifier que la page est rechargée avec une erreur
        self.assertEqual(response.status_code, 200)

        # Vérifier que le message d'erreur est bien présent dans le contenu de la page
        self.assertContains(response, "Veuillez spécifier la durée du contrat pour un CDD")

        # Vérifier qu'aucune offre n'a été créée avec ces données
        self.assertFalse(JobOffer.objects.filter(title=cdd_data['title']).exists())

    def test_invalid_salary_range(self):
        """Test que le formulaire est invalide si le salaire min > salaire max"""
        # Données avec salaire min > salaire max
        invalid_salary_data = self.valid_form_data.copy()
        invalid_salary_data.update({
            'min_salary': 50000,
            'max_salary': 40000
        })

        # Soumettre le formulaire
        response = self.client.post(self.create_url, invalid_salary_data)

        # Vérifier que la page est rechargée avec une erreur
        self.assertEqual(response.status_code, 200)

        # Vérifier que le message d'erreur est bien présent dans le contenu de la page
        self.assertContains(response, "Le salaire maximum doit être supérieur au salaire minimum")

        # Vérifier qu'aucune offre n'a été créée avec ces données
        self.assertFalse(JobOffer.objects.filter(title=invalid_salary_data['title']).exists())

    def test_work_location_property(self):
        """Test que la propriété work_location renvoie l'adresse de l'agence si location est vide"""
        # Créer une offre sans spécifier de lieu
        offer = JobOffer.objects.create(
            title='Test Offer',
            agency=self.agency,
            contract_type='CDI',
            experience_required='JUNIOR',
            description='Test description',
            reference='JF-TEST-1234'
        )

        # Vérifier que work_location renvoie l'adresse de l'agence
        self.assertEqual(offer.work_location, self.agency.address)

        # Modifier le lieu de l'offre
        custom_location = 'Lyon, France'
        offer.location = custom_location
        offer.save()

        # Vérifier que work_location renvoie maintenant le lieu personnalisé
        self.assertEqual(offer.work_location, custom_location)
