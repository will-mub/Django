
from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from sales.models import Sale, SaleItem
from expenses.models import Expense
from produce.models import Produce


@login_required
def reports_dashboard(request):
    # Exclude voided expenses from financial calculations.
    expenses = Expense.objects.filter(is_void=False)

    # Calculate sales revenue from sale items.
    sales_total = SaleItem.objects.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('quantity') * F('unit_price'),
                output_field=DecimalField(
                    max_digits=20,
                    decimal_places=2
                )
            )
        )
    )['total'] or Decimal('0.00')

    expenses_total = expenses.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    estimated_profit = sales_total - expenses_total

    total_sales = Sale.objects.count()
    total_expense_records = expenses.count()

    low_stock = Produce.objects.filter(
        quantity_in_stock__lte=F('reorder_level')
    )

    # Best-selling produce by quantity sold.
    best_sellers = (
        SaleItem.objects.values(
            'produce__name',
            'produce__unit'
        )
        .annotate(
            quantity_sold=Sum('quantity'),
            revenue=Sum(
                ExpressionWrapper(
                    F('quantity') * F('unit_price'),
                    output_field=DecimalField(
                        max_digits=20,
                        decimal_places=2
                    )
                )
            )
        )
        .order_by('-quantity_sold')[:5]
    )

    # Monthly totals for the last six calendar months.
    today = date.today()
    first_month = today.month - 5
    year = today.year

    while first_month <= 0:
        first_month += 12
        year -= 1

    start_date = date(year, first_month, 1)

    monthly_sales = (
        SaleItem.objects
        .filter(sale__sale_date__date__gte=start_date)
        .annotate(month=TruncMonth('sale__sale_date'))
        .values('month')
        .annotate(
            total=Sum(
                ExpressionWrapper(
                    F('quantity') * F('unit_price'),
                    output_field=DecimalField(
                        max_digits=20,
                        decimal_places=2
                    )
                )
            )
        )
        .order_by('month')
    )

    monthly_expenses = (
        expenses.filter(expense_date__gte=start_date)
        .annotate(month=TruncMonth('expense_date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    context = {
        'sales_total': sales_total,
        'expenses_total': expenses_total,
        'estimated_profit': estimated_profit,
        'total_sales': total_sales,
        'total_expense_records': total_expense_records,
        'low_stock': low_stock,
        'low_stock_count': low_stock.count(),
        'best_sellers': best_sellers,
        'monthly_sales': monthly_sales,
        'monthly_expenses': monthly_expenses,
    }

    return render(request, 'reports/dashboard.html', context)
