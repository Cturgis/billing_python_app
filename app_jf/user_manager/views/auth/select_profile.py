from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_manager.forms.select_profile import SelectProfileForm

@login_required
def select_profile(request):
    if request.method == 'POST':
        form = SelectProfileForm(request.POST)
        if form.is_valid():
            profile_type = form.cleaned_data['profile_type']
            request.session['profile_type'] = profile_type


            if profile_type == 'jobseeker':
                return redirect('register_jobseeker')
            else:  # profile_type == 'agency'
                return redirect('register_agency')
    else:
        form = SelectProfileForm()

    return render(request, 'user_manager/select_profile.html', {'form': form})
