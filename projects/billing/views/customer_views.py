from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from billing.models.Customer import Customer
from billing.forms.customer_form import CustomerForm

@login_required
def customer_list(request):
    customers = Customer.objects.select_related('user').all()
    return render(request, 'billing/customer/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client créé avec succès.')
            return redirect('billing:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'billing/customer/customer_form.html', {'form': form})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client mis à jour avec succès.')
            return redirect('billing:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'billing/customer/customer_form.html', {'form': form, 'customer': customer})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Client supprimé avec succès.')
        return redirect('billing:customer_list')
    return render(request, 'billing/customer/customer_confirm_delete.html', {'customer': customer})

