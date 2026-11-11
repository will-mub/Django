"""Database model for farm produce. Each product stores category, stock levels, pricing, and reorder thresholds for inventory control."""

from django.db import models

# Create your models here.


class Produce(models.Model):

    CATEGORY_CHOICES = [
        ('CROP', 'Crop'),
        ('DAIRY', 'Dairy'),
        ('POULTRY', 'Poultry'),
        ('LIVESTOCK', 'Livestock'),
        ('OTHER', 'Other'),
    ]

    UNIT_CHOICES = [
        ('KG', 'Kilograms'),
        ('LITRE', 'Litres'),
        ('BUNCH', 'Bunches'),
        ('TRAY', 'Trays'),
        ('PIECE', 'Pieces'),
        ('BAG', 'Bags'),
    ]

    name = models.CharField(max_length=150)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField(blank=True)

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    quantity_in_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    reorder_level = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=10
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level
