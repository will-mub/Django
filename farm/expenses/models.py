
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('SEEDS', 'Seeds'),
        ('FERTILISER', 'Fertiliser'),
        ('ANIMAL_FEED', 'Animal Feed'),
        ('VETERINARY', 'Veterinary Services'),
        ('LABOUR', 'Labour'),
        ('TRANSPORT', 'Transport'),
        ('EQUIPMENT', 'Equipment'),
        ('MAINTENANCE', 'Maintenance'),
        ('UTILITIES', 'Utilities'),
        ('OTHER', 'Other'),
    ]

    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('CREDIT', 'Credit'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=150)

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    expense_date = models.DateField(default=timezone.localdate)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='CASH'
    )

    description = models.TextField(blank=True)

    receipt_number = models.CharField(
        max_length=100,
        blank=True
    )

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_void = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-expense_date', '-created_at']

    def __str__(self):
        return f"{self.title} - UGX {self.amount}"

    def clean(self):
        super().clean()

        if self.amount is not None and self.amount <= 0:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'amount': 'Expense amount must be greater than zero.'
            })
