from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.contrib import messages
from user_manager.models import JobSeeker, Agency

class ProfileCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_urls = [
            'select_profile',  # Nom correct de l'URL
            'register_jobseeker',  # Nom correct de l'URL
            'register_agency',  # Nom correct de l'URL
            'login',
            'logout',
            'register',
            'admin:',
        ]

        if request.user.is_authenticated:
            try:
                resolver_match = resolve(request.path_info)
                current_url_name = resolver_match.url_name
                current_namespace = resolver_match.namespace

                full_url_name = f"{current_namespace}:{current_url_name}" if current_namespace else current_url_name

                should_check = True
                for excluded in excluded_urls:
                    if current_url_name and excluded in current_url_name:
                        should_check = False
                        break
                    if current_namespace and excluded in current_namespace:
                        should_check = False
                        break
                    if full_url_name and excluded in full_url_name:
                        should_check = False
                        break

                if should_check and current_url_name is not None:
                    if not request.user.groups.exists():
                        if current_url_name != 'select_profile':
                            messages.info(request, "Veuillez d'abord choisir votre type de profil.")
                            return redirect('select_profile')
                    else:
                        group = request.user.groups.first().name

                        if group == 'JobSeeker':
                            try:
                                JobSeeker.objects.get(user=request.user)
                            except JobSeeker.DoesNotExist:
                                if current_url_name != 'register_jobseeker':
                                    messages.info(request, "Veuillez compléter votre profil de demandeur d'emploi.")
                                    return redirect('register_jobseeker')

                        elif group == 'Agency':
                            try:
                                Agency.objects.get(user=request.user)
                            except Agency.DoesNotExist:
                                if current_url_name != 'register_agency':
                                    messages.info(request, "Veuillez compléter votre profil d'entreprise.")
                                    return redirect('register_agency')
            except Exception as e:
                print(f"Erreur dans le middleware ProfileCheck: {str(e)}")
                pass

        response = self.get_response(request)
        return response
