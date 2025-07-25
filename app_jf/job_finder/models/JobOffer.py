from django.db import models
from django.utils import timezone
from user_manager.models.Agency import Agency

class JobOffer(models.Model):
    # Choices pour le type de contrat
    class ContractType(models.TextChoices):
        CDI = 'CDI', 'CDI (Contrat à Durée Indéterminée)'
        CDD = 'CDD', 'CDD (Contrat à Durée Déterminée)'
        FREELANCE = 'FREELANCE', 'Freelance'
        INTERNSHIP = 'INTERNSHIP', 'Stage'
        APPRENTICESHIP = 'APPRENTICESHIP', 'Apprentissage'
        PART_TIME = 'PART_TIME', 'Temps partiel'

    # Choices pour l'expérience requise
    class Experience(models.TextChoices):
        NO_EXPERIENCE = 'NO_EXPERIENCE', 'Débutant (0 an)'
        JUNIOR = 'JUNIOR', 'Junior (< 2 ans)'
        MID_LEVEL = 'MID_LEVEL', 'Intermédiaire (2-4 ans)'
        SENIOR = 'SENIOR', 'Senior (5-8 ans)'
        EXPERT = 'EXPERT', 'Expert (> 10 ans)'

    # Champs du modèle
    title = models.CharField(max_length=255, verbose_name="Intitulé du poste")
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="job_offers", verbose_name="Agence")
    contract_type = models.CharField(max_length=20, choices=ContractType.choices, verbose_name="Type de contrat")
    contract_duration = models.IntegerField(null=True, blank=True, verbose_name="Durée du contrat (en mois)", help_text="Laissez vide pour CDI ou contrat sans durée fixe")
    experience_required = models.CharField(max_length=20, choices=Experience.choices, default=Experience.NO_EXPERIENCE, verbose_name="Expérience requise")
    reference = models.CharField(max_length=50, unique=True, verbose_name="Référence de l'offre")
    publication_date = models.DateTimeField(default=timezone.now, verbose_name="Date de publication")
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salaire minimum")
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salaire maximum")
    description = models.TextField(verbose_name="Description du poste")
    location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Lieu de travail", help_text="Laissez vide pour utiliser l'adresse de l'agence")
    is_active = models.BooleanField(default=True, verbose_name="Offre active")

    class Meta:
        verbose_name = "Offre d'emploi"
        verbose_name_plural = "Offres d'emploi"
        ordering = ['-publication_date']

    def __str__(self):
        return f"{self.title} - {self.agency.name} - Ref: {self.reference}"

    @property
    def salary_range(self):
        """Renvoie la fourchette de salaire formatée"""
        if self.min_salary is None and self.max_salary is None:
            return "Non communiqué"
        elif self.min_salary is None:
            return f"Jusqu'à {self.max_salary} €"
        elif self.max_salary is None:
            return f"À partir de {self.min_salary} €"
        else:
            return f"De {self.min_salary} € à {self.max_salary} €"

    @property
    def work_location(self):
        """Récupère le lieu de travail, utilise l'adresse de l'agence si non spécifié"""
        if self.location:
            return self.location
        return self.agency.address
