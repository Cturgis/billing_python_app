from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from user_manager.models.Agency import Agency
from job_finder.models.JobOffer import JobOffer

@login_required
def agency_offers(request):
    user = request.user

    if not user.groups.filter(name='Agency').exists():
        messages.error(request, "Vous n'avez pas les permissions pour accéder à cette page.")
        return redirect('job_finder:dashboard')

    try:
        agency = Agency.objects.get(user=user)

        job_offers = JobOffer.objects.filter(agency=agency)

        search_query = request.GET.get('search', '')
        contract_filter = request.GET.get('contract_type', '')
        active_filter = request.GET.get('status', '')
        experience_filter = request.GET.get('experience', '')
        sort_by = request.GET.get('sort_by', 'title')  # Par défaut, tri par titre
        sort_by_date = request.GET.get('sort_by_date', 'desc')  # Par défaut, date décroissante (plus récent en premier)

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

        if experience_filter:
            job_offers = job_offers.filter(experience_required=experience_filter)

        total_results = job_offers.count()

        if sort_by == 'publication_date':
            order_prefix = '' if sort_by_date == 'asc' else '-'
            job_offers = job_offers.order_by(f'{order_prefix}publication_date')
        else:
            job_offers = job_offers.order_by(sort_by)

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

        active_filters = bool(contract_filter or active_filter or experience_filter or sort_by != 'title' or sort_by_date != 'desc')

        preserve_params = ''
        non_filter_params = {}
        for key, value in request.GET.items():
            if key not in ['search', 'contract_type', 'status', 'experience', 'sort_by', 'sort_by_date']:
                non_filter_params[key] = value

        if non_filter_params:
            from urllib.parse import urlencode
            preserve_params = urlencode(non_filter_params)

        return render(request, 'job_finder/agency/agency_offers.html', {
            'agency': agency,
            'job_offers': job_offers,
            'search_query': search_query,
            'filters': filters,
            'show_filters': True,
            'active_filters': active_filters,
            'total_results': total_results,
            'reset_url': reverse('job_finder:agency_offers'),
            'contract_filter': contract_filter,
            'active_filter': active_filter,
            'experience_filter': experience_filter,
            'sort_by': sort_by,
            'sort_by_date': sort_by_date,
            'preserve_params': preserve_params
        })

    except Agency.DoesNotExist:
        messages.error(request, "Votre profil d'agence est incomplet. Veuillez contacter un administrateur.")
        return redirect('job_finder:dashboard')
