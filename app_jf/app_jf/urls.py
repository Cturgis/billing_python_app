from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_manager.urls')),
    path('home/', include('job_finder.urls')),
]
