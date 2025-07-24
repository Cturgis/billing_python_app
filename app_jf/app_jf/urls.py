from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path('admin/', admin.site.urls),
    path('user/', include('user_manager.urls')),
    path('home/', include('job_finder.urls')),
]
