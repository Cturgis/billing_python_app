from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qtty = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Produits"

    def __str__(self):
        return f"{self.name} - {self.price}€ (Stock: {self.qtty})"
