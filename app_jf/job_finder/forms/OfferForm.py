from django import forms
from django.utils.crypto import get_random_string
from job_finder.models.JobOffer import JobOffer

class OfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = [
            'title',
            'contract_type',
            'contract_duration',
            'experience_required',
            'min_salary',
            'max_salary',
            'description',
            'location',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Développeur Web Frontend'}),
            'contract_duration': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'min_salary': forms.NumberInput(attrs={'class': 'form-input', 'step': '100', 'min': '0'}),
            'max_salary': forms.NumberInput(attrs={'class': 'form-input', 'step': '100', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8, 'placeholder': 'Décrivez le poste, les missions et les responsabilités...'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Laissez vide pour utiliser l\'adresse de votre agence'}),
        }
        labels = {
            'title': 'Intitulé du poste',
            'contract_type': 'Type de contrat',
            'contract_duration': 'Durée du contrat (en mois)',
            'experience_required': 'Expérience requise',
            'min_salary': 'Salaire minimum (€/an)',
            'max_salary': 'Salaire maximum (€/an)',
            'description': 'Description du poste',
            'location': 'Lieu de travail',
        }
        help_texts = {
            'contract_duration': 'Laissez vide pour un CDI ou un contrat sans durée fixe',
            'min_salary': 'Laissez vide pour ne pas spécifier de minimum',
            'max_salary': 'Laissez vide pour ne pas spécifier de maximum',
            'location': 'Si différent de l\'adresse de votre agence',
        }

    def __init__(self, *args, **kwargs):
        self.agency = kwargs.pop('agency', None)
        super(OfferForm, self).__init__(*args, **kwargs)

        self.fields['contract_duration'].required = False
        self.fields['min_salary'].required = False
        self.fields['max_salary'].required = False
        self.fields['location'].required = False

    def clean(self):
        cleaned_data = super().clean()
        min_salary = cleaned_data.get('min_salary')
        max_salary = cleaned_data.get('max_salary')
        contract_type = cleaned_data.get('contract_type')
        contract_duration = cleaned_data.get('contract_duration')

        if min_salary and max_salary and min_salary > max_salary:
            self.add_error('max_salary', "Le salaire maximum doit être supérieur au salaire minimum.")

        if contract_type == 'CDD' and not contract_duration:
            self.add_error('contract_duration', "Veuillez spécifier la durée du contrat pour un CDD.")

        return cleaned_data

    def save(self, commit=True):
        instance = super(OfferForm, self).save(commit=False)

        if self.agency:
            instance.agency = self.agency

        if not instance.pk:
            from datetime import date
            today = date.today().strftime('%Y%m%d')
            random_suffix = get_random_string(4).upper()
            instance.reference = f"JF-{today}-{random_suffix}"

        if commit:
            instance.save()

        return instance
