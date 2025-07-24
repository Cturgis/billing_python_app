from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from user_manager.forms.register import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            login(request, user)

            messages.success(request, "Compte créé avec succès. Veuillez compléter votre profil.")
            return redirect('select_profile')
    else:
        form = RegisterForm()
    return render(request, 'user_manager/register.html', {'form': form})
