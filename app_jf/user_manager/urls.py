from django.urls import path
from user_manager.views.auth.login import login

urlpatterns = [
    path('login/', login, name='login'),
]
