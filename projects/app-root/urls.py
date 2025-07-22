from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_billing(request):
    return redirect('billing:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('billing/', include('billing.urls')),
    path('', redirect_to_billing),
]