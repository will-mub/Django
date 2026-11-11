"""Admin configuration for customer records. The model is registered here so staff can search and manage clients from the Django admin panel."""

from django.contrib import admin

# Register your models here.
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_number',
        'email',
    )

    search_fields = ('full_name', 'phone_number')