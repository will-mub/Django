"""Database model for farm suppliers. Each supplier stores business details used for ordering stock and managing vendors."""


from django.db import models


class Supplier(models.Model):

    SUPPLIER_TYPES = [
        ('SEEDS', 'Seeds'),
        ('FERTILISER', 'Fertiliser'),
        ('ANIMAL_FEED', 'Animal Feed'),
        ('EQUIPMENT', 'Farm Equipment'),
        ('VETERINARY', 'Veterinary Supplies'),
        ('GENERAL', 'General Supplies'),
    ]

    name = models.CharField(max_length=150)
    supplier_type = models.CharField(
        max_length=30,
        choices=SUPPLIER_TYPES,
        default='GENERAL'
    )
    contact_person = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

