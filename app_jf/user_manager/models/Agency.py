from django.db import models
from django.conf import settings

class Agency(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agency_profile')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    siret = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.name