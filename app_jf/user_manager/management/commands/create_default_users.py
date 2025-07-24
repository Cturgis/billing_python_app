from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from user_manager.models import Agency, JobSeeker


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
            Agency.objects.create(user=agency_user, name='Agence Démo', address='1 rue de l’Emploi, Paris',
                                  siret='12345678901234')
            # Création du profil JobSeeker pour agency
            JobSeeker.objects.create(user=agency_user, birthDate='1980-01-01', city='Lyon')
            self.stdout.write(
                self.style.SUCCESS('Agency créée, profils Agency et JobSeeker associés, ajoutée au groupe Agency'))
        else:
            agency_user = User.objects.get(username='agency')
            agency_user.groups.add(agency_group)
            if not hasattr(agency_user, 'agency_profile'):
                Agency.objects.create(user=agency_user, name='Agence Démo', address='1 rue de l’Emploi, Paris',
                                      siret='12345678901234')
            if not hasattr(agency_user, 'jobseeker_profile'):
                JobSeeker.objects.create(user=agency_user, birthDate='1980-01-01', city='Lyon')
            self.stdout.write('Agency existe déjà, profils Agency et JobSeeker vérifiés, ajoutée au groupe Agency')
