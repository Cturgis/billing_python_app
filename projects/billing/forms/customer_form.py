from django import forms
from billing.models.Customer import Customer
from django.contrib.auth.models import User, Group

class CustomerForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Nom d\'utilisateur')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
    is_admin = forms.BooleanField(label="Utilisateur admin", required=False)

    class Meta:
        model = Customer
        fields = ['address']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True):
        # If updating, get the existing user
        if self.instance and self.instance.pk:
            user = self.instance.user
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
        else:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
            if self.cleaned_data.get('is_admin'):
                group, _ = Group.objects.get_or_create(name='admin')
            else:
                group, _ = Group.objects.get_or_create(name='customer')
            user.groups.add(group)
        customer = super().save(commit=False)
        customer.user = user
        if commit:
            customer.save()
        return customer
