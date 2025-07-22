from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from billing.models.Customer import Customer
from billing.models.Product import Product
from billing.models.Invoice import Invoice, InvoiceItem

@login_required
def shop_view(request):
    products = Product.objects.order_by('pk')
    customer = get_object_or_404(Customer, user=request.user)
    if request.method == 'POST':
        ordered = False
        invoice = Invoice.objects.create(customer=customer)
        for product in products:
            qtty_str = request.POST.get(f'qtty_{product.pk}', '0')
            try:
                qtty = int(qtty_str)
            except ValueError:
                qtty = 0
            if qtty > 0:
                if qtty > product.qtty:
                    messages.warning(request, f"Stock insuffisant pour {product.name} (stock: {product.qtty})")
                    continue
                item = InvoiceItem.objects.create(
                    invoice=invoice, product=product,
                    quantity=qtty, unit_price=product.price
                )
                ordered = True
        if ordered:
            messages.success(request, "Votre commande a été validée !")
            return redirect('billing:customer_shop')
        else:
            invoice.delete()
            messages.warning(request, "Aucun produit sélectionné ou stock insuffisant.")
            return redirect('billing:customer_shop')
    return render(request, 'billing/customer/customer_shop.html', {'products': products})

