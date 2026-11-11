"""Produce views and inventory operations. The app exposes pages for listing products, creating entries, and deleting old stock records."""


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Produce
from .forms import ProduceForm


@login_required
def produce_list(request):

    search = request.GET.get('search', '')

    products = Produce.objects.all().order_by('-created_at')

    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'produce/list.html', {
        'products': products,
        'search': search,
    })


@login_required
def produce_create(request):

    if request.method == 'POST':
        form = ProduceForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Produce successfully registered.'
            )

            return redirect('produce_list')

    else:
        form = ProduceForm()

    return render(request, 'produce/form.html', {
        'form': form,
        'title': 'Add New Produce',
    })


@login_required
def produce_update(request, pk):

    product = get_object_or_404(Produce, pk=pk)

    if request.method == 'POST':
        form = ProduceForm(request.POST, instance=product)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Produce successfully updated.'
            )

            return redirect('produce_list')

    else:
        form = ProduceForm(instance=product)

    return render(request, 'produce/form.html', {
        'form': form,
        'title': 'Update Produce',
    })


@login_required
def produce_delete(request, pk):

    product = get_object_or_404(Produce, pk=pk)

    if request.method == 'POST':
        product.delete()

        messages.success(
            request,
            'Produce successfully deleted.'
        )

        return redirect('produce_list')

    return render(request, 'produce/confirm_delete.html', {
        'product': product,
    })
