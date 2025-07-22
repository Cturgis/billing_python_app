from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from billing.models.Product import Product
from billing.forms.product_form import ProductForm


@login_required
def product_list(request):
    products = Product.objects.all()
    edit_id = request.GET.get('edit_id')
    return render(request, 'billing/product/product_list.html', {'products': products, 'edit_id': edit_id})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit créé avec succès.')
            return redirect('billing:product_list')
    else:
        form = ProductForm()
    return render(request, 'billing/product/product_form.html', {'form': form})


def product_update_price(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            new_price = float(request.POST['price'])
            if new_price >= 0:
                product.price = new_price
                product.save()
                messages.success(request, f'Prix de {product.name} mis à jour à {product.price} €.')
            else:
                messages.error(request, 'Le prix ne peut pas être négatif.')
        except (ValueError, KeyError):
            messages.error(request, 'Valeur de prix invalide.')
    return redirect('billing:product_list')


@login_required
def product_update_qtty(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            new_qtty = int(request.POST['qtty'])
            if new_qtty >= 0:
                product.qtty = new_qtty
                product.save()
                messages.success(request, f'Quantité de {product.name} mise à jour à {product.qtty}.')
            else:
                messages.error(request, 'La quantité ne peut pas être négative.')
        except (ValueError, KeyError):
            messages.error(request, 'Valeur de quantité invalide.')
    return redirect('billing:product_list')


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit mis à jour avec succès.')
            return redirect('billing:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'billing/product/product_form.html', {'form': form, 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produit supprimé avec succès.')
        return redirect('billing:product_list')
    return render(request, 'billing/product/product_confirm_delete.html', {'product': product})


@login_required
def product_increment(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.qtty += 1
    product.save()
    messages.success(request, f'Quantité de {product.name} augmentée à {product.qtty}.')
    return redirect('billing:product_list')


@login_required
def product_decrement(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.qtty > 0:
        product.qtty -= 1
        product.save()
        messages.success(request, f'Quantité de {product.name} diminuée à {product.qtty}.')
    else:
        messages.warning(request, f'La quantité de {product.name} est déjà à zéro.')
    return redirect('billing:product_list')
