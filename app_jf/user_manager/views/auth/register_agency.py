from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from user_manager.forms.register_agency import RegisterAgencyForm
from user_manager.models import Agency

@login_required
def register_agency(request):
    if request.method == 'POST':
        form = RegisterAgencyForm(request.POST)
        if form.is_valid():
            agency = form.save(commit=False)
            agency.user = request.user
            agency.save()
            agency_group, _ = Group.objects.get_or_create(name='Agency')
            request.user.groups.add(agency_group)

            messages.success(request, "Votre profil d'entreprise a été créé avec succès.")
            return redirect('job_finder:dashboard')
    else:
        form = RegisterAgencyForm()

    return render(request, 'user_manager/register_agency.html', {'form': form})
