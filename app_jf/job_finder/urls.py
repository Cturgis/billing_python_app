from django.urls import path
from job_finder.views.dashboard import dashboard
from job_finder.views.agency_offers import agency_offers
from job_finder.views.create_offer import create_offer

app_name = 'job_finder'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('agency/offers/', agency_offers, name='agency_offers'),
    path('agency/offers/create/', create_offer, name='create_offer'),
]
