from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    user = request.user
    group = user.groups.first().name if user.groups.exists() else 'Aucun groupe'
    return render(request, 'job_finder/dashboard.html', {
        'user': user,
        'group': group,
    })

