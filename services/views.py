from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubscriptionPlan
from .forms import SubscriptionPlanForm


@login_required(login_url='/auth/login/')
def subscription_plan_list(request):
    # Filtering by plan type
    plan_type_filter = request.GET.get('plan_type', 'all')
    query = request.GET.get('q', '')
    per_page = request.GET.get('per_page', 25)

    # Fetch and filter subscription plans based on search query and plan type
    plans = SubscriptionPlan.objects.all()
    if plan_type_filter == 'pppoe':
        plans = plans.filter(plan_type='pppoe')
    elif plan_type_filter == 'hotspot':
        plans = plans.filter(plan_type='hotspot')

    # Apply search filtering
    if query:
        plans = plans.filter(
            Q(name__icontains=query) |
            Q(upload_speed__icontains=query) |
            Q(download_speed__icontains=query)
        )

    # Pagination
    paginator = Paginator(plans, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Initialize form for creating a new plan in a modal
    form = SubscriptionPlanForm()

    return render(request, 'services/subscription_plan_list.html', {
        'page_obj': page_obj,
        'query': query,
        'plan_type_filter': plan_type_filter,
        'per_page': int(per_page),
        'form': form,
    })


@login_required(login_url='/auth/login/')
def subscription_plan_create(request):
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscription plan created successfully.")
            return redirect('services:subscription_plan_list')
    else:
        form = SubscriptionPlanForm()
    return render(request, 'services/subscription_plan_form.html', {'form': form, 'title': 'Create Subscription Plan'})


@login_required(login_url='/auth/login/')
def subscription_plan_edit(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscription plan updated successfully.")
            return redirect('services:subscription_plan_list')
    else:
        form = SubscriptionPlanForm(instance=plan)
    return render(request, 'services/subscription_plan_form.html', {'form': form, 'title': 'Edit Subscription Plan'})


@login_required(login_url='/auth/login/')
def subscription_plan_delete(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, "Subscription plan deleted successfully.")
        return redirect('services:subscription_plan_list')
    return render(request, 'services/subscription_plan_confirm_delete.html', {'plan': plan})


@login_required(login_url='/auth/login/')
def subscription_plan_detail(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)
    return render(request, 'services/subscription_plan_detail.html', {'plan': plan})
