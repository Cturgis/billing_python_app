from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from user_manager.models.Agency import Agency
from job_finder.models.JobOffer import JobOffer

@login_required
def agency_offers(request):
    """
    Affiche toutes les offres d'emploi de l'agence de l'utilisateur connecté.
    L'utilisateur doit appartenir au groupe 'Agency' pour accéder à cette vue.
    """
    user = request.user

    if not user.groups.filter(name='Agency').exists():
        messages.error(request, "Vous n'avez pas les permissions pour accéder à cette page.")
        return redirect('job_finder:dashboard')

    try:
        # Récupérer l'agence associée à l'utilisateur
        agency = Agency.objects.get(user=user)

        # Récupérer toutes les offres d'emploi de cette agence
        job_offers = JobOffer.objects.filter(agency=agency).order_by('-publication_date')

        return render(request, 'job_finder/agency/agency_offers.html', {
            'agency': agency,
            'job_offers': job_offers,
        })

    except Agency.DoesNotExist:
        messages.error(request, "Votre profil d'agence est incomplet. Veuillez contacter un administrateur.")
        return redirect('job_finder:dashboard')
