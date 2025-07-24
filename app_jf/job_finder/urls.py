from django.urls import path
from job_finder.views.dashboard import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
]

