"""Database model for a farm customer. Each record keeps the buyer's personal and contact information so sales can be linked to a person."""


from django.db import models


class Customer(models.Model):

    full_name = models.CharField(max_length=150)

    phone_number = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

