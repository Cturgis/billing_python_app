from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_manager.models.Agency import Agency
from job_finder.forms.OfferForm import OfferForm

@login_required
def create_offer(request):
    user = request.user

    if not user.groups.filter(name='Agency').exists():
        messages.error(request, "Vous n'avez pas les permissions pour créer une offre d'emploi.")
        return redirect('job_finder:dashboard')

    try:
        agency = Agency.objects.get(user=user)

        if request.method == 'POST':
            form = OfferForm(request.POST, agency=agency)

            if form.is_valid():
                offer = form.save()
                messages.success(request, f"L'offre d'emploi '{offer.title}' (Réf: {offer.reference}) a été créée avec succès.")
                return redirect('job_finder:agency_offers')
        else:
            form = OfferForm(agency=agency)

        return render(request, 'job_finder/agency/create_offer.html', {
            'form': form,
            'agency': agency,
        })

    except Agency.DoesNotExist:
        messages.error(request, "Votre profil d'agence est incomplet. Veuillez contacter un administrateur.")
        return redirect('job_finder:dashboard')
