"""Admin configuration for produce records. This register helps administrators keep product stock and pricing manageable in the backend."""

from django.contrib import admin

# Register your models here.
from .models import Produce


@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'selling_price',
        'quantity_in_stock',
        'unit',
    )

    list_filter = ('category', 'unit')

    search_fields = ('name',)