"""Sales views and transaction logic. This module manages the list, creation, and detail pages for customer purchases."""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404

from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemFormSet


@login_required
def sale_list(request):
    sales = Sale.objects.select_related('customer').prefetch_related(
        'items__produce'
    )

    search = request.GET.get('search', '').strip()

    if search:
        sales = sales.filter(customer__full_name__icontains=search)

    return render(request, 'sales/list.html', {
        'sales': sales,
        'search': search,
    })


@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            items = [
                item_form
                for item_form in formset.forms
                if item_form.cleaned_data
                and not item_form.cleaned_data.get('DELETE', False)
                and item_form.cleaned_data.get('produce')
            ]

            if not items:
                form.add_error(None, 'Add at least one produce item.')

            else:
                total = sum(
                    (
                        item.cleaned_data['quantity']
                        * item.cleaned_data['unit_price']
                        for item in items
                    ),
                    Decimal('0.00')
                )

                amount_paid = form.cleaned_data['amount_paid']

                if amount_paid > total:
                    form.add_error(
                        'amount_paid',
                        'Amount paid cannot exceed the sale total.'
                    )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        sale = form.save(commit=False)
                        sale.created_by = request.user
                        sale.save()

                        for item_form in items:
                            produce = item_form.cleaned_data['produce']
                            quantity = item_form.cleaned_data['quantity']

                            # Deduct stock only if enough stock is available.
                            updated = type(produce).objects.filter(
                                pk=produce.pk,
                                quantity_in_stock__gte=quantity
                            ).update(
                                quantity_in_stock=(
                                    F('quantity_in_stock') - quantity
                                )
                            )

                            if updated == 0:
                                raise ValidationError(
                                    f'Insufficient stock for {produce.name}. '
                                    'Please check the available quantity.'
                                )

                            sale_item = item_form.save(commit=False)
                            sale_item.sale = sale
                            sale_item.save()

                    messages.success(
                        request,
                        'Sale recorded successfully and stock updated.'
                    )
                    return redirect('sale_list')

                except ValidationError as error:
                    form.add_error(None, error.message)

    else:
        form = SaleForm()
        formset = SaleItemFormSet()

    return render(request, 'sales/form.html', {
        'form': form,
        'formset': formset,
        'page_title': 'Record New Sale',
    })


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(
        Sale.objects.select_related('customer').prefetch_related(
            'items__produce'
        ),
        pk=pk
    )

    return render(request, 'sales/detail.html', {'sale': sale})