"""Admin configuration for sales records. The sales entity is made available in the admin dashboard for operational oversight."""

from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'sale_date',
        'amount_paid',
    )

    list_filter = ('sale_date', 'payment_method')
    search_fields = ('customer__full_name',)
    inlines = [SaleItemInline]


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = (
        'sale',
        'produce',
        'quantity',
        'unit_price',
    )