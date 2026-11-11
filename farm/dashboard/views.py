"""Dashboard home view. It summarizes key inventory and customer metrics for the farm's main landing page."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from produce.models import Produce
from customers.models import Customer
from django.db import models


@login_required
def home(request):

    total_produce = Produce.objects.count()

    total_customers = Customer.objects.count()

    low_stock = Produce.objects.filter(
        quantity_in_stock__lte=models.F('reorder_level')
    ).count()

    context = {
        'total_produce': total_produce,
        'total_customers': total_customers,
        'low_stock': low_stock,
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )
