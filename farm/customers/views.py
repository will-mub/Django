"""Customer views and CRUD logic. These functions render customer listings and handle create, update, and delete actions for the farm's client records."""


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Customer
from .forms import CustomerForm


@login_required
def customer_list(request):
    search = request.GET.get('search', '')

    customers = Customer.objects.all().order_by('-created_at')

    if search:
        customers = customers.filter(
            full_name__icontains=search
        ) | customers.filter(
            phone_number__icontains=search
        )

    return render(request, 'customers/list.html', {
        'customers': customers,
        'search': search,
    })


@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Customer added successfully.')
        return redirect('customer_list')

    return render(request, 'customers/form.html', {
        'form': form,
        'page_title': 'Add New Customer',
    })


@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Customer updated successfully.')
        return redirect('customer_list')

    return render(request, 'customers/form.html', {
        'form': form,
        'page_title': 'Edit Customer',
    })


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully.')
        return redirect('customer_list')

    return render(request, 'customers/confirm_delete.html', {
        'customer': customer,
    })
