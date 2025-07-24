from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from user_manager.forms.login import LoginForm
from user_manager.models import JobSeeker, Agency


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)

                if not user.groups.exists():
                    messages.info(request, "Veuillez choisir votre type de profil.")
                    return redirect('select_profile')

                group = user.groups.first().name
                messages.success(request, f"Connexion réussie en tant que {group}")

                if group == 'JobSeeker':
                    try:
                        JobSeeker.objects.get(user=user)
                        return redirect('job_finder:dashboard')
                    except JobSeeker.DoesNotExist:
                        messages.info(request, "Veuillez compléter votre profil de demandeur d'emploi.")
                        return redirect('register_jobseeker')

                elif group == 'Agency':
                    try:
                        Agency.objects.get(user=user)
                        return redirect('job_finder:dashboard')
                    except Agency.DoesNotExist:
                        messages.info(request, "Veuillez compléter votre profil d'entreprise.")
                        return redirect('register_agency')

                return redirect('dashboard')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'user_manager/login.html', {'form': form})
