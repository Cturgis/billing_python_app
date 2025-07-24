from django import forms

class SelectProfileForm(forms.Form):
    PROFILE_TYPE_CHOICES = [
        ('jobseeker', 'Je suis un particulier à la recherche d\'emploi'),
        ('agency', 'Je suis une entreprise qui recrute')
    ]
    profile_type = forms.ChoiceField(
        choices=PROFILE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Veuillez choisir votre profil"
    )
