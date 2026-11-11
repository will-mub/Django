
from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'amount',
        'expense_date',
        'payment_method',
        'is_void',
    )

    list_filter = (
        'category',
        'payment_method',
        'expense_date',
        'is_void',
    )

    search_fields = (
        'title',
        'receipt_number',
        'description',
    )

    readonly_fields = ('created_at',)
