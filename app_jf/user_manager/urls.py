from django.urls import path
from user_manager.views.auth.login import login
from user_manager.views.auth.logout import logout
from user_manager.views.auth.register import register

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]
