from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from reportlab.pdfgen import canvas
from .models import Invoice, Quotation, Payment, SubscriptionPlan, CustomItem
from .forms import InvoiceForm, QuotationForm, PaymentForm, SubscriptionPlanForm, CustomItemForm
from django.db.models import Sum, Count



class BillingDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'billing/dashboard.html'
    login_url = '/auth_app/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate total revenue (sum of all payments received)
        context['total_revenue'] = Payment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0

        # Calculate outstanding payments (sum of unpaid invoices)
        context['outstanding_payments'] = Invoice.objects.filter(status='Pending').aggregate(total=Sum('amount_due'))[
                                              'total'] or 0

        # Count the number of invoices and payments
        context['invoice_count'] = Invoice.objects.count()
        context['payments_received'] = Payment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0

        # Retrieve recent invoices
        context['recent_invoices'] = Invoice.objects.order_by('-created_at')[:5]

        # Retrieve recent payments
        context['recent_payments'] = Payment.objects.order_by('-payment_date')[:5]

        # Revenue Over Time (For the Chart)
        # Assume you're tracking payments by date
        revenue_data = Payment.objects.extra(select={'day': "DATE(payment_date)"}).values('day').annotate(
            total=Sum('amount_paid')).order_by('day')
        context['revenue_labels'] = [data['day'].strftime('%Y-%m-%d') for data in revenue_data]
        context['revenue_data'] = [data['total'] for data in revenue_data]

        # Payment Status Breakdown (For the Pie Chart)
        paid_count = Invoice.objects.filter(status='Paid').count()
        pending_count = Invoice.objects.filter(status='Pending').count()
        overdue_count = Invoice.objects.filter(status='Overdue').count()

        context['payment_status_data'] = [paid_count, pending_count, overdue_count]

        return context


# Invoice Views
class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'billing/invoice_list.html'
    paginate_by = 10
    login_url = '/auth_app/login/'

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'billing/invoice_form.html'
    success_url = reverse_lazy('invoice_list')
    login_url = '/auth_app/login/'

class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'billing/invoice_form.html'
    success_url = reverse_lazy('invoice_list')
    login_url = '/auth_app/login/'

class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'billing/invoice_confirm_delete.html'
    success_url = reverse_lazy('invoice_list')
    login_url = '/auth_app/login/'


# Quotation Views
class QuotationListView(LoginRequiredMixin, ListView):
    model = Quotation
    template_name = 'billing/quotation_list.html'
    paginate_by = 10
    login_url = '/auth_app/login/'

class QuotationCreateView(LoginRequiredMixin, CreateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_form.html'
    success_url = reverse_lazy('quotation_list')
    login_url = '/auth_app/login/'

class QuotationUpdateView(LoginRequiredMixin, UpdateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_form.html'
    success_url = reverse_lazy('quotation_list')
    login_url = '/auth_app/login/'

class QuotationDeleteView(LoginRequiredMixin, DeleteView):
    model = Quotation
    template_name = 'billing/quotation_confirm_delete.html'
    success_url = reverse_lazy('quotation_list')
    login_url = '/auth_app/login/'


# Payment Views
class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'billing/payment_list.html'
    paginate_by = 10
    login_url = '/auth_app/login/'

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'billing/payment_form.html'
    success_url = reverse_lazy('payment_list')
    login_url = '/auth_app/login/'

class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'billing/payment_form.html'
    success_url = reverse_lazy('payment_list')
    login_url = '/auth_app/login/'

class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'billing/payment_confirm_delete.html'
    success_url = reverse_lazy('payment_list')
    login_url = '/auth_app/login/'


# Subscription Plan Views
class SubscriptionPlanListView(LoginRequiredMixin, ListView):
    model = SubscriptionPlan
    template_name = 'billing/subscription_plan_list.html'
    paginate_by = 10
    login_url = '/auth_app/login/'

class SubscriptionPlanCreateView(LoginRequiredMixin, CreateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = 'billing/subscription_plan_form.html'
    success_url = reverse_lazy('subscription_plan_list')
    login_url = '/auth_app/login/'

class SubscriptionPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = 'billing/subscription_plan_form.html'
    success_url = reverse_lazy('subscription_plan_list')
    login_url = '/auth_app/login/'

class SubscriptionPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = SubscriptionPlan
    template_name = 'billing/subscription_plan_confirm_delete.html'
    success_url = reverse_lazy('subscription_plan_list')
    login_url = '/auth_app/login/'


# Custom Item Views
class CustomItemListView(LoginRequiredMixin, ListView):
    model = CustomItem
    template_name = 'billing/custom_item_list.html'
    paginate_by = 10
    login_url = '/auth_app/login/'

class CustomItemCreateView(LoginRequiredMixin, CreateView):
    model = CustomItem
    form_class = CustomItemForm
    template_name = 'billing/custom_item_form.html'
    success_url = reverse_lazy('custom_item_list')
    login_url = '/auth_app/login/'

class CustomItemUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomItem
    form_class = CustomItemForm
    template_name = 'billing/custom_item_form.html'
    success_url = reverse_lazy('custom_item_list')
    login_url = '/auth_app/login/'

class CustomItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomItem
    template_name = 'billing/custom_item_confirm_delete.html'
    success_url = reverse_lazy('custom_item_list')
    login_url = '/auth_app/login/'


# PDF Generation Views
@login_required(login_url='/auth_app/login/')
def generate_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_id}.pdf"'

    # Create a PDF document
    p = canvas.Canvas(response)
    p.drawString(100, 750, f"Invoice ID: {invoice.invoice_id}")
    p.drawString(100, 730, f"Customer: {invoice.customer.name}")
    p.drawString(100, 710, f"Amount Due: {invoice.amount_due}")
    p.drawString(100, 690, f"Status: {invoice.status}")

    # Finalize the PDF
    p.showPage()
    p.save()

    return response


@login_required(login_url='/auth_app/login/')
def generate_quotation_pdf(request, quotation_id):
    quotation = get_object_or_404(Quotation, quotation_id=quotation_id)

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="quotation_{quotation.quotation_id}.pdf"'

    # Create a PDF document
    p = canvas.Canvas(response)
    p.drawString(100, 750, f"Quotation ID: {quotation.quotation_id}")
    p.drawString(100, 730, f"Customer: {quotation.customer.name}")
    p.drawString(100, 710, f"Amount Due: {quotation.amount_due}")
    p.drawString(100, 690, f"Status: {quotation.status}")

    # Finalize the PDF
    p.showPage()
    p.save()

    return response


@login_required(login_url='/auth_app/login/')
def generate_report(request):
    # Your report generation logic here
    return HttpResponse("Report generated successfully.")
