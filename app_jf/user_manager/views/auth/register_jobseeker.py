from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from user_manager.forms.register_jobseeker import RegisterJobSeekerForm
from user_manager.models import JobSeeker

@login_required
def register_jobseeker(request):
    if request.method == 'POST':
        form = RegisterJobSeekerForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            jobseeker_group, _ = Group.objects.get_or_create(name='JobSeeker')
            request.user.groups.add(jobseeker_group)

            messages.success(request, "Votre profil a été complété avec succès.")
            return redirect('job_finder:dashboard')
    else:
        form = RegisterJobSeekerForm()

    return render(request, 'user_manager/register_jobseeker.html', {'form': form})
