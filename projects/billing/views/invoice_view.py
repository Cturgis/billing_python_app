from projects.billing.models import Customer, Invoice, Product
from projects.billing.models.Invoice import InvoiceItem


def create_invoice_with_products(customer_id, products_data):
    # products_data = [{'product_id': 1, 'quantity': 2}, {'product_id': 3, 'quantity': 1}]

    customer = Customer.objects.get(id=customer_id)
    invoice = Invoice.objects.create(customer=customer)

    for item_data in products_data:
        product = Product.objects.get(id=item_data['product_id'])
        InvoiceItem.objects.create(
            invoice=invoice,
            product=product,
            quantity=item_data['quantity']
            # unit_price sera automatiquement défini dans save()
        )

    return invoice


def invoice_detail(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    items = invoice.invoiceitem_set.select_related('product').all()

    context = {
        'invoice': invoice,
        'items': items,
        'total': invoice.total_amount()
    }
    return render(request, 'billing/invoice_detail.html', context)
