from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")
    birthDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date de naissance")
    city = forms.CharField(max_length=100, label="Ville")

    class Meta:
        model = get_user_model()
        fields = [
            'email', 'username', 'password', 'confirm_password',
            'first_name', 'last_name', 'birthDate', 'city',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _("Les mots de passe ne correspondent pas."))
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Un utilisateur avec cette adresse e-mail existe déjà.")
        return email
