from django import forms
from billing.models.Customer import Customer
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Nom d\'utilisateur')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

    class Meta:
        model = Customer
        fields = ['address']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        customer = super().save(commit=False)
        customer.user = user
        if commit:
            customer.save()
        return customer
