from django.urls import path
from user_manager.views.auth.login import login
from user_manager.views.auth.logout import logout
from user_manager.views.auth.register import register
from user_manager.views.auth.register_agency import register_agency
from user_manager.views.auth.select_profile import select_profile
from user_manager.views.auth.register_jobseeker import register_jobseeker
from user_manager.views.auth.register_agency import register_agency

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('select-profile/', select_profile, name='select_profile_type'),
    path('register-jobseeker/', register_jobseeker, name='register_jobseeker'),
    path('register-agency/', register_agency, name='register_agency'),
]
