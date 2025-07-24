from django import forms
from user_manager.models import JobSeeker

class RegisterJobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['birthDate', 'city']
        labels = {
            'birthDate': 'Date de naissance',
            'city': 'Ville'
        }
        widgets = {
            'birthDate': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('birthDate')
        city = cleaned_data.get('city')

        if not birth_date:
            self.add_error('birthDate', 'Ce champ est obligatoire')

        if not city:
            self.add_error('city', 'Ce champ est obligatoire')

        return cleaned_data
