from django import forms
from user_manager.models import Agency

class RegisterAgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['name', 'address', 'siret']
        labels = {
            'name': "Nom de l'entreprise",
            'address': "Adresse",
            'siret': "SIRET",
        }

