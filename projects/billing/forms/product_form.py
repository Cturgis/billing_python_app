from django import forms
from billing.models.Product import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'qtty']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'qtty': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

