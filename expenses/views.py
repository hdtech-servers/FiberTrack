from datetime import datetime, timedelta
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.timezone import now
from calendar import month_abbr

from .models import Expense, ExpenseCategory, Budget, ExpenseLog
from .forms import ExpenseForm, ExpenseCategoryForm, BudgetForm, ExpenseLogFilterForm
from .services import MPesaService
from django.db.models import Sum, F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth


# Utility: Render Modal Forms
def render_modal_form(request, template_name, form):
    return JsonResponse({
        'html_form': render_to_string(template_name, {'form': form}, request=request)
    })


### Dashboard ###
@login_required
def dashboard(request):
    # Total Expenses
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    # Recent Expenses
    recent_expenses = Expense.objects.order_by('-date')[:3]

    # Category Breakdown
    category_data = (
        Expense.objects.values('category__name')
        .annotate(total_amount=Sum('amount'))
        .order_by('-total_amount')
    )
    category_labels = [data['category__name'] for data in category_data]
    category_values = [float(data['total_amount']) for data in category_data]  # Convert Decimal to float

    # Monthly Expense Trend
    current_year = now().year
    monthly_data = (
        Expense.objects.filter(date__year=current_year)
        .values('date__month')
        .annotate(total_amount=Sum('amount'))
        .order_by('date__month')
    )
    month_labels = [f"Month {data['date__month']}" for data in monthly_data]
    month_values = [float(data['total_amount']) for data in monthly_data]  # Convert Decimal to float

    return render(request, 'expenses/dashboard.html', {
        'total_expenses': total_expenses,
        'recent_expenses': recent_expenses,
        'category_labels': json.dumps(category_labels),
        'category_values': json.dumps(category_values),
        'month_labels': json.dumps(month_labels),
        'month_values': json.dumps(month_values),
    })
@login_required
def expense_trend_data(request):
    period = request.GET.get('period', 'daily')  # Default to 'daily'
    if period == 'weekly':
        data = (
            Expense.objects.annotate(period=TruncWeek('date'))
            .values('period')
            .annotate(total=Sum('amount'))
            .order_by('period')
        )
    elif period == 'monthly':
        data = (
            Expense.objects.annotate(period=TruncMonth('date'))
            .values('period')
            .annotate(total=Sum('amount'))
            .order_by('period')
        )
    else:  # Default to daily
        data = (
            Expense.objects.annotate(period=TruncDay('date'))
            .values('period')
            .annotate(total=Sum('amount'))
            .order_by('period')
        )

    labels = [item['period'].strftime('%Y-%m-%d') for item in data]
    values = [item['total'] for item in data]
    return JsonResponse({'labels': labels, 'data': values})


@login_required
def expense_list(request):
    # Query all expenses
    expenses = Expense.objects.all().order_by('-date')

    # Filter by start and end date
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        expenses = expenses.filter(category_id=category_id)

    # Pagination
    page_size = request.GET.get('page_size', 25)
    paginator = Paginator(expenses, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Form handling for adding expenses
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.created_by = request.user
                expense.last_updated_by = request.user
                expense.save()
                messages.success(request, "Expense created successfully.")
                return redirect('expense_list')
            except Exception as e:
                messages.error(request, f"Unexpected error: {str(e)}")
        else:
            messages.error(request, "There were errors in your form. Please fix them and try again.")
    else:
        form = ExpenseForm()

    # Pass context to the template
    categories = ExpenseCategory.objects.all()
    return render(request, 'expenses/expense_list.html', {
        'page_obj': page_obj,
        'page_size': page_size,
        'create_expense_form': form,
        'categories': categories,
        'filter_form': {
            'start_date': start_date,
            'end_date': end_date,
            'category': category_id
        }
    })

@login_required
def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    return render(request, 'expenses/expense_detail.html', {
        'expense': expense,
        'supplier': expense.supplier,
        'created_by': expense.created_by,
        'last_updated_by': expense.last_updated_by,
        'created_at': expense.created_at,
        'updated_at': expense.updated_at
    })


@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.created_by = request.user
                expense.last_updated_by = request.user
                expense.save()
                messages.success(request, "Expense created successfully.")
                return JsonResponse({'success': True})
            except Exception as e:
                # Log the error to console or logging system
                print(f"Error saving expense: {e}")
                return JsonResponse({'success': False, 'errors': f"Unexpected error: {str(e)}"})
        else:
            # Log form validation errors
            print("Form errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ExpenseForm()
    return render_modal_form(request, 'expenses/partial_expense_create.html', form)


@login_required
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            expense.last_updated_by = request.user
            expense.save()
            messages.success(request, "Expense updated successfully.")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ExpenseForm(instance=expense)
    return render_modal_form(request, 'expenses/partial_expense_update.html', form)


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully.")
        return JsonResponse({'success': True})
    return render_modal_form(request, 'expenses/partial_expense_delete.html', {'expense': expense})


### Expense Category Views ###
@login_required
def category_list(request):
    categories = ExpenseCategory.objects.all().order_by('name')
    page_size = request.GET.get('page_size', 25)
    paginator = Paginator(categories, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Instantiate forms
    create_category_form = ExpenseCategoryForm()

    return render(request, 'expenses/category_list.html', {
        'page_obj': page_obj,
        'page_size': page_size,
        'create_category_form': create_category_form,
    })


@login_required
def create_category(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'html_form': render_to_string('expenses/partial_category_form.html', {'form': form}, request=request)})
    else:
        form = ExpenseCategoryForm()
        return JsonResponse({'html_form': render_to_string('expenses/partial_category_form.html', {'form': form}, request=request)})

@login_required
def update_category(request, category_id):
    category = get_object_or_404(ExpenseCategory, id=category_id)
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ExpenseCategoryForm(instance=category)
    return JsonResponse({'html_form': render(request, 'expenses/partial_category_form.html', {'form': form}).content.decode()})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(ExpenseCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return JsonResponse({'success': True})
    return JsonResponse({'html_form': render(request, 'expenses/partial_category_delete.html', {'category': category}).content.decode()})


### Budget Views ###
@login_required
def budget_list(request):
    budgets = Budget.objects.all().order_by('-year', '-month')
    return render(request, 'expenses/budget_list.html', {'budgets': budgets})


@login_required
def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget created successfully.")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = BudgetForm()
    return render_modal_form(request, 'expenses/partial_budget_create.html', form)


### Log View ###
@login_required
def expense_log_list(request):
    form = ExpenseLogFilterForm(request.GET or None)
    logs = ExpenseLog.objects.all().order_by('-timestamp')

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        operation = form.cleaned_data.get('operation')

        if start_date:
            logs = logs.filter(timestamp__gte=start_date)
        if end_date:
            logs = logs.filter(timestamp__lte=end_date)
        if operation:
            logs = logs.filter(operation=operation)

    return render(request, 'expenses/expense_log_list.html', {'logs': logs, 'form': form})


@login_required
def initiate_b2c_payment(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    phone_number = expense.supplier.phone
    amount = expense.amount
    reference = f"Expense-{expense.id}"

    try:
        response = MPesaService.initiate_b2c_payment(phone_number, amount, reference)
        messages.success(request, "B2C payment initiated successfully.")
    except Exception as e:
        messages.error(request, str(e))
    return redirect('expense_detail', expense_id=expense.id)

@login_required
def initiate_b2b_payment(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    shortcode = expense.supplier.paybill_number  # Example: Assuming paybill is set
    amount = expense.amount
    reference = f"Expense-{expense.id}"

    try:
        response = MPesaService.initiate_b2b_payment(shortcode, amount, reference)
        messages.success(request, "B2B payment initiated successfully.")
    except Exception as e:
        messages.error(request, str(e))
    return redirect('expense_detail', expense_id=expense.id)

def b2c_result_callback(request):
    """Handle B2C Result URL callbacks."""
    try:
        data = json.loads(request.body)
        # Log the response and update expense status
        print(data)
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Acknowledged"})
    except Exception as e:
        return JsonResponse({"ResultCode": 1, "ResultDesc": str(e)})

def b2b_result_callback(request):
    """Handle B2B Result URL callbacks."""
    try:
        data = json.loads(request.body)
        # Log the response and update expense status
        print(data)
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Acknowledged"})
    except Exception as e:
        return JsonResponse({"ResultCode": 1, "ResultDesc": str(e)})

