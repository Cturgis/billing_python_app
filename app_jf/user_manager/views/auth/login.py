from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from user_manager.forms.login import LoginForm

from job_finder.views.dashboard import dashboard


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                group = user.groups.first().name if user.groups.exists() else 'Aucun groupe'
                messages.success(request, f"Connexion réussie en tant que {group}")
                return redirect('job_finder:dashboard')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'user_manager/login.html', {'form': form})
