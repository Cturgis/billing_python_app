from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from user_manager.models.Agency import Agency
from job_finder.models.JobOffer import JobOffer

@login_required
def agency_offers(request):
    """
    Affiche toutes les offres d'emploi de l'agence de l'utilisateur connecté.
    L'utilisateur doit appartenir au groupe 'Agency' pour accéder à cette vue.
    Prend en charge la recherche et le filtrage des offres.
    """
    user = request.user

    if not user.groups.filter(name='Agency').exists():
        messages.error(request, "Vous n'avez pas les permissions pour accéder à cette page.")
        return redirect('job_finder:dashboard')

    try:
        # Récupérer l'agence associée à l'utilisateur
        agency = Agency.objects.get(user=user)

        # Récupérer toutes les offres d'emploi de cette agence
        job_offers = JobOffer.objects.filter(agency=agency)

        # Paramètres de recherche et filtrage
        search_query = request.GET.get('search', '')
        contract_filter = request.GET.get('contract_type', '')
        active_filter = request.GET.get('status', '')

        # Appliquer les filtres à la requête
        if search_query:
            job_offers = job_offers.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(reference__icontains=search_query)
            )

        if contract_filter:
            job_offers = job_offers.filter(contract_type=contract_filter)

        if active_filter:
            is_active = active_filter == 'active'
            job_offers = job_offers.filter(is_active=is_active)

        # Compter les résultats après filtrage
        total_results = job_offers.count()

        # Trier par date de publication décroissante
        job_offers = job_offers.order_by('-publication_date')

        # Construire les options de filtre pour le template
        contract_types = [
            {'value': 'CDI', 'label': 'CDI', 'selected': contract_filter == 'CDI'},
            {'value': 'CDD', 'label': 'CDD', 'selected': contract_filter == 'CDD'},
            {'value': 'FREELANCE', 'label': 'Freelance', 'selected': contract_filter == 'FREELANCE'},
            {'value': 'INTERNSHIP', 'label': 'Stage', 'selected': contract_filter == 'INTERNSHIP'},
            {'value': 'APPRENTICESHIP', 'label': 'Apprentissage', 'selected': contract_filter == 'APPRENTICESHIP'},
            {'value': 'PART_TIME', 'label': 'Temps partiel', 'selected': contract_filter == 'PART_TIME'},
        ]

        status_options = [
            {'value': 'active', 'label': 'Actives', 'selected': active_filter == 'active'},
            {'value': 'inactive', 'label': 'Inactives', 'selected': active_filter == 'inactive'},
        ]

        filters = [
            {'id': 'contract_type', 'name': 'contract_type', 'label': 'Type de contrat', 'options': contract_types},
            {'id': 'status', 'name': 'status', 'label': 'Statut', 'options': status_options}
        ]

        # Vérifier si des filtres sont actifs
        active_filters = bool(contract_filter or active_filter)

        return render(request, 'job_finder/agency/agency_offers.html', {
            'agency': agency,
            'job_offers': job_offers,
            'search_query': search_query,
            'filters': filters,
            'show_filters': True,
            'active_filters': active_filters,
            'total_results': total_results,
            'reset_url': reverse('job_finder:agency_offers')
        })

    except Agency.DoesNotExist:
        messages.error(request, "Votre profil d'agence est incomplet. Veuillez contacter un administrateur.")
        return redirect('job_finder:dashboard')
