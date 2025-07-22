from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from .Customer import Customer
from .Product import Product


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='InvoiceItem')
    paid = models.BooleanField(default=False)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.0, help_text="TVA")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Facture #{self.pk} - {self.customer} - {self.total_amount}€"

    def get_absolute_url(self):
        return reverse('billing:invoice_detail', kwargs={'pk': self.pk})

    @property
    def total_amount(self):
        total = 0
        for item in self.invoiceitem_set.all():
            total += item.subtotal()
        return total + (total * self.vat_rate / 100)

    def total_items(self):
        return sum(item.quantity for item in self.invoiceitem_set.all())


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Pour garder le prix au moment de la commande

    class Meta:
        unique_together = ('invoice', 'product')

    def __str__(self):
        return f"{self.product.name} x{self.quantity} @ {self.unit_price}€"

    def subtotal(self):
        return self.quantity * self.unit_price

    def clean(self):
        if self.product and self.quantity > self.product.qtty:
            raise ValidationError(
                f"Quantité demandée ({self.quantity}) supérieure au stock disponible ({self.product.qtty})"
            )

    def save(self, *args, **kwargs):
        if not self.unit_price and self.product:
            self.unit_price = self.product.price

        self.full_clean()
        super().save(*args, **kwargs)

        if self.product:
            self.product.qtty -= self.quantity
            self.product.save()
