from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from billing.forms.auth_forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='admin').exists():
            return redirect('billing:dashboard')
        elif request.user.groups.filter(name='customer').exists():
            return redirect('billing:customer_dashboard')
        else:
            return redirect('billing:logout')

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.get_username()} !')

                if user.groups.filter(name='admin').exists():
                    return redirect('billing:dashboard')
                elif user.groups.filter(name='customer').exists():
                    return redirect('billing:customer_dashboard')
                else:
                    return redirect('billing:logout')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')

    return render(request, 'billing/auth/login.html', {'form': form})


@login_required
def logout_view(request):
    username = request.user.get_full_name() or request.user.username
    logout(request)
    messages.success(request, f'Au revoir {username} ! Vous êtes maintenant déconnecté.')
    return redirect('billing:login')


@login_required
def dashboard(request):
    return render(request, 'billing/dashboard.html', {
        'user': request.user
    })
