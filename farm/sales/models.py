"""Database models for sales and sale items. Together they track customer purchases, pricing, payment status, and linked product quantities."""

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from customers.models import Customer
from produce.models import Produce


class Sale(models.Model):

    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('OTHER', 'Other'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='sales',
        null=True,
        blank=True
    )

    sale_date = models.DateTimeField(auto_now_add=True)

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='CASH'
    )

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sale_date']

    def __str__(self):
        return f"Sale #{self.pk}"

    @property
    def total_amount(self):
        total = sum(
            (item.line_total for item in self.items.all()),
            Decimal('0.00')
        )
        return total

    @property
    def balance(self):
        return self.total_amount - self.amount_paid

    @property
    def payment_status(self):
        if self.amount_paid <= 0:
            return 'Unpaid'
        elif self.amount_paid < self.total_amount:
            return 'Partially Paid'
        return 'Paid'

    def clean(self):
        if self.amount_paid < 0:
            raise ValidationError({
                'amount_paid': 'Amount paid cannot be negative.'
            })


class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    produce = models.ForeignKey(
        Produce,
        on_delete=models.PROTECT,
        related_name='sale_items'
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.produce.name} - {self.quantity}"

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError({
                'quantity': 'Quantity must be greater than zero.'
            })

        if self.unit_price < 0:
            raise ValidationError({
                'unit_price': 'Unit price cannot be negative.'
            })