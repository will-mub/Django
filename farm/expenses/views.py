from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Expense
from .forms import ExpenseForm


@login_required
def expense_list(request):
    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()

    expenses = Expense.objects.filter(is_void=False)

    if search:
        expenses = expenses.filter(
            Q(title__icontains=search) |
            Q(receipt_number__icontains=search) |
            Q(description__icontains=search)
        )

    if category:
        expenses = expenses.filter(category=category)

    total_expenses = expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(request, 'expenses/list.html', {
        'expenses': expenses,
        'search': search,
        'category': category,
        'categories': Expense.CATEGORY_CHOICES,
        'total_expenses': total_expenses,
    })


@login_required
def expense_create(request):
    form = ExpenseForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        expense = form.save(commit=False)
        expense.recorded_by = request.user
        expense.save()

        messages.success(request, 'Expense recorded successfully.')
        return redirect('expense_list')

    return render(request, 'expenses/form.html', {
        'form': form,
        'page_title': 'Record New Expense',
    })


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(
        Expense,
        pk=pk,
        is_void=False
    )

    form = ExpenseForm(request.POST or None, instance=expense)

    if request.method == 'POST' and form.is_valid():
        form.save()

        messages.success(request, 'Expense updated successfully.')
        return redirect('expense_list')

    return render(request, 'expenses/form.html', {
        'form': form,
        'page_title': 'Edit Expense',
    })


@login_required
def expense_void(request, pk):
    expense = get_object_or_404(
        Expense,
        pk=pk,
        is_void=False
    )

    if request.method == 'POST':
        expense.is_void = True
        expense.save(update_fields=['is_void'])

        messages.success(
            request,
            'Expense has been voided. Its record has been retained.'
        )
        return redirect('expense_list')

    return render(request, 'expenses/confirm_void.html', {
        'expense': expense,
    })