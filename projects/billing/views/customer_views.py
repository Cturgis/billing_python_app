from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from billing.models.Customer import Customer
from billing.models.Product import Product
from billing.models.Invoice import Invoice, InvoiceItem
from billing.forms.customer_form import CustomerForm
from django.utils import timezone


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


# testing
@login_required
def customer_dashboard(request):
    return render(request, 'billing/customer/customer_dashboard.html')


@login_required
def shop_view(request):
    products = Product.objects.order_by('pk')
    customer = get_object_or_404(Customer, user=request.user)
    if request.method == 'POST':
        ordered = False
        today = timezone.now().date()
        invoice, created = Invoice.objects.get_or_create(customer=customer, created_at__date=today, defaults={})
        for product in products:
            qtty_str = request.POST.get(f'qtty_{product.pk}', '0')
            try:
                qtty = int(qtty_str)
            except ValueError:
                qtty = 0
            if qtty > 0:
                # Check stock
                if qtty > product.qtty:
                    messages.warning(request, f"Stock insuffisant pour {product.name} (stock: {product.qtty})")
                    continue
                # Create or update InvoiceItem
                item, item_created = InvoiceItem.objects.get_or_create(
                    invoice=invoice, product=product,
                    defaults={'quantity': 0, 'unit_price': product.price}
                )
                if item_created:
                    item.quantity = qtty
                else:
                    item.quantity += qtty
                item.unit_price = product.price
                item.save()
                # Decrement stock
                product.qtty -= qtty
                product.save()
                ordered = True
        if ordered:
            messages.success(request, "Votre commande a été validée !")
        else:
            messages.warning(request, "Aucun produit sélectionné ou stock insuffisant.")
        return redirect('billing:customer_shop')
    return render(request, 'billing/customer/customer_shop.html', {'products': products})


@login_required
def my_invoice_view(request):
    customer = get_object_or_404(Customer, user=request.user)
    invoices = Invoice.objects.filter(customer=customer).order_by('-created_at')
    return render(request, 'billing/customer/customer_invoice.html', {'invoices': invoices})


@login_required
def buy_product_view(request, product_id):
    customer = get_object_or_404(Customer, user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    try:
        qtty = int(request.POST.get('qtty', 1))
    except (TypeError, ValueError):
        qtty = 1
    if qtty < 1:
        messages.error(request, "Quantité invalide.")
        return redirect('billing:shop')

    today = timezone.now().date()
    invoice, created = Invoice.objects.get_or_create(customer=customer, created_at__date=today, defaults={})

    item, item_created = InvoiceItem.objects.get_or_create(invoice=invoice, product=product, defaults={'quantity': 0})
    item.quantity += qtty
    item.save()
    messages.success(request, f"{qtty} x {product.name} ajouté à votre facture.")
    return redirect('billing:shop')
