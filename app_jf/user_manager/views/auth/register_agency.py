from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from user_manager.forms.agency_register import AgencyRegisterForm
from user_manager.models import Agency

@login_required
def register_agency(request):
    user = request.user
    if hasattr(user, 'agency_profile'):
        messages.info(request, "Vous avez déjà une agence associée à votre compte.")
        return redirect('login')
    if request.method == 'POST':
        if 'skip' in request.POST:
            return redirect('login')
        form = AgencyRegisterForm(request.POST)
        if form.is_valid():
            agency = form.save(commit=False)
            agency.user = user
            agency.save()
            agency_group, _ = Group.objects.get_or_create(name='Agency')
            user.groups.add(agency_group)
            messages.success(request, "Agence créée et associée à votre compte.")
            return redirect('login')
    else:
        form = AgencyRegisterForm()
    return render(request, 'user_manager/register_agency.html', {'form': form})

