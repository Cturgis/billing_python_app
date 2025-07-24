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
