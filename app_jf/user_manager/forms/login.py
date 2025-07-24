from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Le nom d'utilisateur est obligatoire")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Le mot de passe est obligatoire")
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect")

        return cleaned_data
