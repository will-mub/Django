"""Admin configuration for supplier information. This register makes supplier records searchable and manageable in the admin panel."""


from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'supplier_type',
        'contact_person',
        'phone_number',
        'is_active',
        'created_at',
    )

    list_filter = ('supplier_type', 'is_active')
    search_fields = ('name', 'phone_number', 'contact_person')
