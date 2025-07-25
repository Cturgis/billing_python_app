from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from user_manager.models import Agency, JobSeeker
from job_finder.models.JobOffer import JobOffer
import random
from datetime import date, timedelta
from django.utils.crypto import get_random_string
from django.utils import timezone


class Command(BaseCommand):
    help = 'Crée les utilisateurs et groupes par défaut (Admin, Agency, JobSeeker) et un profil Agency.'

    def handle(self, *args, **options):
        User = get_user_model()
        # Création des groupes
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        agency_group, _ = Group.objects.get_or_create(name='Agency')
        jobseeker_group, _ = Group.objects.get_or_create(name='JobSeeker')

        # Création de l'admin
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword',
                                                       first_name='Admin', last_name='User')
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('Admin créé et ajouté au groupe Admin'))
        else:
            admin_user = User.objects.get(username='admin')
            admin_user.groups.add(admin_group)
            self.stdout.write('Admin existe déjà, ajouté au groupe Admin')

        # Création d'un JobSeeker
        if not User.objects.filter(username='jobseeker').exists():
            jobseeker_user = User.objects.create_user('jobseeker', 'jobseeker@example.com', 'jobseekerpassword',
                                                      first_name='Jean', last_name='Chercheur')
            jobseeker_user.groups.add(jobseeker_group)
            # Création du profil JobSeeker
            JobSeeker.objects.create(user=jobseeker_user, birthDate='1990-01-01', city='Paris')
            self.stdout.write(self.style.SUCCESS('JobSeeker créé, profil associé et ajouté au groupe JobSeeker'))
        else:
            jobseeker_user = User.objects.get(username='jobseeker')
            jobseeker_user.groups.add(jobseeker_group)
            if not hasattr(jobseeker_user, 'jobseeker_profile'):
                JobSeeker.objects.create(user=jobseeker_user, birthDate='1990-01-01', city='Paris')
            self.stdout.write('JobSeeker existe déjà, ajouté au groupe JobSeeker et profil vérifié')

        # Création d'une Agency
        if not User.objects.filter(username='agency').exists():
            agency_user = User.objects.create_user('agency', 'agency@example.com', 'agencypassword',
                                                   first_name='Entreprise', last_name='Demo')
            agency_user.groups.add(agency_group)
            agency = Agency.objects.create(user=agency_user, name='TechFun Innovations', address='42 rue de l\'Emploi, Paris',
                                  siret='12345678901234')
            # Création du profil JobSeeker pour agency
            JobSeeker.objects.create(user=agency_user, birthDate='1980-01-01', city='Lyon')

            # Création de 10 offres d'emploi pour cette agence
            self.create_job_offers(agency)

            self.stdout.write(
                self.style.SUCCESS('Agency créée, profils Agency et JobSeeker associés, ajoutée au groupe Agency'))
        else:
            agency_user = User.objects.get(username='agency')
            agency_user.groups.add(agency_group)
            try:
                agency = Agency.objects.get(user=agency_user)
                # Vérifier s'il existe déjà des offres pour cette agence
                if not JobOffer.objects.filter(agency=agency).exists():
                    self.create_job_offers(agency)
            except Agency.DoesNotExist:
                agency = Agency.objects.create(user=agency_user, name='TechFun Innovations',
                                     address='42 rue de l\'Emploi, Paris', siret='12345678901234')
                self.create_job_offers(agency)

            if not hasattr(agency_user, 'jobseeker_profile'):
                JobSeeker.objects.create(user=agency_user, birthDate='1980-01-01', city='Lyon')
            self.stdout.write('Agency existe déjà, profils Agency et JobSeeker vérifiés, ajoutée au groupe Agency')

    def create_job_offers(self, agency):
        """Crée 10 offres d'emploi aléatoires et humoristiques pour l'agence"""

        # Liste de titres de poste humoristiques
        titles = [
            "Dompteur de bugs",
            "Magicien du code",
            "Architecte de châteaux de cartes (numériques)",
            "Thérapeute pour ordinateurs dépressifs",
            "Expert en café et développement",
            "Acrobate full-stack",
            "Guru de la procrastination productive",
            "Chuchoteur de serveurs",
            "Philosophe des algorithmes",
            "Ninja du pixel",
            "Maître Yoda du JavaScript",
            "Interprète Python-Humain"
        ]

        # Types de contrat possibles
        contract_types = ['CDI', 'CDD', 'FREELANCE', 'INTERNSHIP']

        # Niveaux d'expérience
        experience_levels = ['NO_EXPERIENCE', 'JUNIOR', 'MID_LEVEL', 'SENIOR', 'EXPERT']

        # Liste de descriptions humoristiques
        descriptions = [
            "Vous êtes capable de transformer du café en code ? Ce poste est fait pour vous ! Nous recherchons quelqu'un qui peut parler aux ordinateurs même quand ils sont de mauvaise humeur.",
            "Rejoignez-nous pour créer des applications si intuitives que même votre grand-mère pourrait les utiliser sans ses lunettes.",
            "Nous cherchons un ninja du code capable de résoudre des bugs tout en restant zen, même quand tout part en spaghetti.",
            "Si vous pouvez expliquer la récursion à un enfant de 5 ans, et que vous savez quand NE PAS utiliser la récursion, nous avons besoin de vous !",
            "Votre mission, si vous l'acceptez : transformer nos idées folles en produits qui fonctionnent réellement. Bonus si vous arrivez à faire croire au client que c'était facile.",
            "Vous aimez les défis impossibles ? Nos délais le sont aussi ! Rejoignez notre équipe pour transformer l'impossible en 'juste très difficile'.",
            "Nous recherchons quelqu'un capable de maintenir un code legacy écrit par des développeurs qui ont mystérieusement disparu (probablement sur une île déserte après avoir vu le code).",
            "Expert recherché pour comprendre notre base de code. Personne ne sait comment ça fonctionne, mais ça marche. Ne pas toucher au code du vendredi !",
            "Vous avez des super-pouvoirs en résolution de problèmes et une cape n'est pas nécessaire (mais appréciée lors des réunions d'équipe).",
            "Si vous pouvez comprendre nos spécifications client et les transformer en quelque chose d'utilisable, vous êtes probablement un être surnaturel. Postulez quand même."
        ]

        # Lieux de travail possibles (vides pour utiliser l'adresse de l'agence, ou spécifiques)
        locations = [
            "",  # Utiliser l'adresse de l'agence
            "Télétravail depuis votre grotte secrète",
            "Paris - à côté des meilleurs cafés",
            "Lyon - capitale de la gastronomie (et du code gourmet)",
            "Bordeaux - où le code coule comme le vin",
            "Dans notre vaisseau spatial en orbite",
        ]

        # Créer 10 offres
        created_count = 0
        for i in range(10):
            # Choisir un type de contrat
            contract_type = random.choice(contract_types)

            # Déterminer la durée si CDD
            contract_duration = None
            if contract_type == 'CDD':
                contract_duration = random.randint(1, 24)  # Entre 1 et 24 mois

            # Salaires aléatoires
            has_salary = random.choice([True, False])
            min_salary = None
            max_salary = None
            if has_salary:
                min_salary = random.randint(30000, 60000)
                max_salary = min_salary + random.randint(5000, 30000)

            # Générer référence unique
            today = date.today().strftime('%Y%m%d')
            random_suffix = get_random_string(4).upper()
            reference = f"JF-{today}-{random_suffix}"

            # Date de publication (entre aujourd'hui et il y a 30 jours)
            days_ago = random.randint(0, 30)
            pub_date = timezone.now() - timedelta(days=days_ago)

            # Créer l'offre
            JobOffer.objects.create(
                title=random.choice(titles),
                agency=agency,
                contract_type=contract_type,
                contract_duration=contract_duration,
                experience_required=random.choice(experience_levels),
                reference=reference,
                publication_date=pub_date,
                min_salary=min_salary,
                max_salary=max_salary,
                description=random.choice(descriptions),
                location=random.choice(locations),
                is_active=random.choice([True, True, True, False])  # 75% de chances d'être actif
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'{created_count} offres d\'emploi créées pour l\'agence {agency.name}'))
