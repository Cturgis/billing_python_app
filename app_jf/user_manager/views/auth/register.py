from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import get_user_model
from user_manager.forms.register import RegisterForm
from user_manager.models import JobSeeker


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
            # Création du profil JobSeeker
            JobSeeker.objects.create(
                user=user,
                birthDate=form.cleaned_data['birthDate'],
                city=form.cleaned_data['city']
            )
            # Ajout au groupe JobSeeker
            jobseeker_group, _ = Group.objects.get_or_create(name='JobSeeker')
            user.groups.add(jobseeker_group)
            messages.success(request, "Inscription réussie. Veuillez compléter les informations de votre entreprise ou passer cette étape.")
            return redirect('register_agency')
    else:
        form = RegisterForm()
    return render(request, 'user_manager/register.html', {'form': form})
