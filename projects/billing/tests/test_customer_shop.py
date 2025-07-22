from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from billing.models.Customer import Customer
from billing.models.Product import Product
from billing.models.Invoice import Invoice, InvoiceItem

class CustomerShopTestCase(TestCase):
    def setUp(self):
        # Create customer group and user
        customer_group, _ = Group.objects.get_or_create(name='customer')
        self.user = User.objects.create_user(username='shopper', password='testpass')
        self.user.groups.add(customer_group)
        self.customer = Customer.objects.create(user=self.user, address='1 rue test')
        # Create products
        self.product1 = Product.objects.create(name='TomateTest', price=10.0, qtty=5)
        self.product2 = Product.objects.create(name='SteakTest', price=20.0, qtty=2)
        self.client = Client()
        self.client.login(username='shopper', password='testpass')

    def test_shop_page_loads(self):
        response = self.client.get('/billing/customer/boutique/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Boutique')
        self.assertContains(response, self.product1.name)

    def test_valid_order_creates_invoice_and_items(self):
        response = self.client.post('/billing/customer/boutique/', {
            f'qtty_{self.product1.pk}': '2',
            f'qtty_{self.product2.pk}': '1',
        }, follow=True)
        # self.assertContains(response, 'Votre commande a été validée')
        invoice = Invoice.objects.get(customer=self.customer)
        item1 = InvoiceItem.objects.get(invoice=invoice, product=self.product1)
        item2 = InvoiceItem.objects.get(invoice=invoice, product=self.product2)
        self.assertEqual(item1.quantity, 2)
        self.assertEqual(item2.quantity, 1)
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.qtty, 3)
        self.assertEqual(self.product2.qtty, 1)

    # def test_order_with_insufficient_stock(self):
    #     response = self.client.post('/billing/customer/boutique/', {
    #         f'qtty_{self.product1.pk}': '10',  # More than stock
    #     }, follow=True)
    #     self.assertContains(response, 'Stock insuffisant')
    #     self.assertFalse(Invoice.objects.filter(customer=self.customer).exists())
    #
    # def test_order_with_no_selection(self):
    #     response = self.client.post('/billing/customer/boutique/', {}, follow=True)
    #     self.assertContains(response, 'Aucun produit sélectionné')
    #     self.assertFalse(Invoice.objects.filter(customer=self.customer).exists())
    #
