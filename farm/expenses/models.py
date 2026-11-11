from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone


class Expense(models.Model):
    """A single farm expense record."""

    # Allowed expense categories (stored value, display label)
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

    # Ways the expense can be paid
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('BANK', 'Bank Transfer'),
        ('CREDIT', 'Credit'),
        ('OTHER', 'Other'),
    ]

    # Short name of the expense
    title = models.CharField(max_length=150)

    # What the money was spent on
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    # Amount in UGX; must be at least 0.01
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    # Date the expense happened (defaults to today)
    expense_date = models.DateField(default=timezone.localdate)

    # How it was paid (defaults to cash)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='CASH'
    )

    # Optional extra details
    description = models.TextField(blank=True)

    # Optional receipt or invoice reference
    receipt_number = models.CharField(
        max_length=100,
        blank=True
    )

    # User who logged the expense; kept as null if the user is deleted
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Marks cancelled entries without deleting them
    is_void = models.BooleanField(default=False)

    # Set automatically when the record is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Newest expenses first
        ordering = ['-expense_date', '-created_at']

    def __str__(self):
        # Readable label, e.g. "Maize seeds - UGX 50000.00"
        return f"{self.title} - UGX {self.amount}"

    def clean(self):
        # Extra validation: amount must be positive
        super().clean()

        if self.amount is not None and self.amount <= 0:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'amount': 'Expense amount must be greater than zero.'
            })
