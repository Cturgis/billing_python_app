from django.urls import path
from user_manager.views.auth.login import login
from user_manager.views.auth.logout import logout
from user_manager.views.auth.register import register
from user_manager.views.auth.register_agency import register_agency
from user_manager.views.auth.select_profile_type import select_profile_type
from user_manager.views.auth.complete_jobseeker_profile import complete_jobseeker_profile
from user_manager.views.auth.complete_agency_profile import complete_agency_profile

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('register-agency/', register_agency, name='register_agency'),
    path('select-profile-type/', select_profile_type, name='select_profile_type'),
    path('complete-jobseeker-profile/', complete_jobseeker_profile, name='complete_jobseeker_profile'),
    path('complete-agency-profile/', complete_agency_profile, name='complete_agency_profile'),
]
