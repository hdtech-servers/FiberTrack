from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, ExpenseCategory
from .forms import ExpenseForm, ExpenseCategoryForm
from django.http import JsonResponse



# List and Create Expense
@login_required(login_url='/auth/login/')
def list_expenses(request):
    expenses = Expense.objects.all()
    categories = ExpenseCategory.objects.all()
    return render(request, 'expenses/list_expenses.html', {'expenses': expenses, 'categories': categories})


@login_required(login_url='/auth/login/')
def add_expense(request):
    categories = ExpenseCategory.objects.all()
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            # Regular form submission (non-AJAX)
            return redirect('list_expenses')
        else:
            # Handle form errors for AJAX requests
            if request.is_ajax():
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return render(request, 'expenses/add_expense.html', {'form': form, 'categories': categories})




# Edit Expense
@login_required(login_url='/auth/login/')
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/edit_expense_modal.html', {'form': form})

# Delete Expense
@login_required(login_url='/auth/login/')
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return JsonResponse({'success': True})


# List and Create Expense Category (Refactored to expenses_category_list)
def expenses_category_list(request):
    categories = ExpenseCategory.objects.all()
    form = ExpenseCategoryForm()
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses_category_list')
    return render(request, 'expenses/expenses_category_list.html', {'categories': categories, 'form': form})

# Edit Expense Category
def expenses_category_edit(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('expenses_category_list')
    else:
        form = ExpenseCategoryForm(instance=category)
    return render(request, 'expenses/expenses_category_form.html', {'form': form})

# Delete Expense Category
def expenses_category_delete(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('expenses_category_list')
    return render(request, 'expenses/expenses_category_confirm_delete.html', {'category': category})