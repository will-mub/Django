"""Supplier views and management logic. The app provides list, add, edit, and soft-delete flows for vendor records."""

from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib import messages  # type: ignore

from .models import Supplier
from .forms import SupplierForm


@login_required
def supplier_list(request):
    search = request.GET.get('search', '').strip()

    suppliers = Supplier.objects.all()
#
    if search:
        suppliers = suppliers.filter(
            models.Q(name__icontains=search) |
            models.Q(phone_number__icontains=search) |
            models.Q(contact_person__icontains=search)
        )

    return render(request, 'suppliers/list.html', {
        'suppliers': suppliers,
        'search': search,
    })


@login_required
def supplier_create(request):
    form = SupplierForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Supplier added successfully.')
        return redirect('supplier_list')

    return render(request, 'suppliers/form.html', {
        'form': form,
        'page_title': 'Add New Supplier',
    })


@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Supplier updated successfully.')
        return redirect('supplier_list')

    return render(request, 'suppliers/form.html', {
        'form': form,
        'page_title': 'Edit Supplier',
    })


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        supplier.is_active = False
        supplier.save(update_fields=['is_active'])
        messages.success(request, 'Supplier marked as inactive.')
        return redirect('supplier_list')

    return render(request, 'suppliers/confirm_delete.html', {
        'supplier': supplier,
    })
