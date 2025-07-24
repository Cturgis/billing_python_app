from django.db import models
from django.conf import settings
from .Agency import Agency

class JobSeeker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobseeker_profile')
    birthDate = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} (JobSeeker)"
