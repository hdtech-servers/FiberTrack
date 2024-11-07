from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from reportlab.pdfgen import canvas
from django.db.models import Sum

from customers.models import Customer
from .models import Invoice, Quotation, Payment, CustomItem
from services.models import SubscriptionPlan
from .forms import InvoiceForm, QuotationForm, PaymentForm, CustomItemForm, CustomItemFormSet


# Dashboard View
class BillingDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'billing/dashboard.html'
    login_url = '/auth_app/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_revenue'] = Payment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0
        context['outstanding_payments'] = Invoice.objects.filter(status='Pending').aggregate(total=Sum('amount_due'))[
                                              'total'] or 0
        context['invoice_count'] = Invoice.objects.count()
        context['payments_received'] = Payment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0
        context['recent_invoices'] = Invoice.objects.order_by('-created_at')[:5]
        context['recent_payments'] = Payment.objects.order_by('-payment_date')[:5]

        revenue_data = Payment.objects.extra(select={'day': "DATE(payment_date)"}).values('day').annotate(
            total=Sum('amount_paid')).order_by('day')
        context['revenue_labels'] = [data['day'].strftime('%Y-%m-%d') for data in revenue_data]
        context['revenue_data'] = [data['total'] for data in revenue_data]

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
    success_url = reverse_lazy('billing:invoice_list')
    login_url = '/auth_app/login/'


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'billing/invoice_form.html'
    success_url = reverse_lazy('billing:invoice_list')
    login_url = '/auth_app/login/'


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'billing/invoice_confirm_delete.html'
    success_url = reverse_lazy('billing:invoice_list')
    login_url = '/auth_app/login/'


# Quotation Views with Custom Item Inline Support
class QuotationListView(LoginRequiredMixin, ListView):
    model = Quotation
    template_name = 'billing/quotation_list.html'
    paginate_by = 10
    login_url = '/auth_app/login/'


# View to select a customer before creating a quotation
class CustomerSelectView(ListView):
    model = Customer
    template_name = 'billing/select_customer.html'
    context_object_name = 'customers'


class QuotationDetailView(DetailView):
    model = Quotation
    template_name = 'billing/quotation_detail.html'
    context_object_name = 'quotation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()  # Assuming related_name='items' on CustomItem model
        return context


# View to create a quotation with items for a selected customer
class QuotationCreateView(CreateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.customer_id = kwargs.get('customer_id')
        self.customer = get_object_or_404(Customer, pk=self.customer_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = CustomItemFormSet(self.request.POST)
        else:
            context['item_formset'] = CustomItemFormSet()
        context['customer'] = self.customer
        return context

    def form_valid(self, form):
        form.instance.customer = self.customer
        response = super().form_valid(form)
        item_formset = CustomItemFormSet(self.request.POST, instance=self.object)
        if item_formset.is_valid():
            item_formset.save()
        else:
            return self.form_invalid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('quotation_list')

class QuotationUpdateView(UpdateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_edit.html'
    success_url = reverse_lazy('billing:quotation_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['item_formset'] = CustomItemFormSet(self.request.POST, instance=self.object)
        else:
            data['item_formset'] = CustomItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        if item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class QuotationDeleteView(LoginRequiredMixin, DeleteView):
    model = Quotation
    template_name = 'billing/quotation_confirm_delete.html'
    success_url = reverse_lazy('billing:quotation_list')
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
    success_url = reverse_lazy('billing:payment_list')
    login_url = '/auth_app/login/'


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'billing/payment_form.html'
    success_url = reverse_lazy('billing:payment_list')
    login_url = '/auth_app/login/'


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'billing/payment_confirm_delete.html'
    success_url = reverse_lazy('billing:payment_list')
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
    success_url = reverse_lazy('billing:custom_item_list')
    login_url = '/auth_app/login/'


class CustomItemUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomItem
    form_class = CustomItemForm
    template_name = 'billing/custom_item_form.html'
    success_url = reverse_lazy('billing:custom_item_list')
    login_url = '/auth_app/login/'


class CustomItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomItem
    template_name = 'billing/custom_item_confirm_delete.html'
    success_url = reverse_lazy('billing:custom_item_list')
    login_url = '/auth_app/login/'


# PDF Generation Views
@login_required(login_url='/auth_app/login/')
def generate_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_id}.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 750, f"Invoice ID: {invoice.invoice_id}")
    p.drawString(100, 730, f"Customer: {invoice.customer.name}")
    p.drawString(100, 710, f"Amount Due: {invoice.amount_due}")
    p.drawString(100, 690, f"Status: {invoice.status}")
    p.showPage()
    p.save()
    return response


@login_required(login_url='/auth_app/login/')
def generate_quotation_pdf(request, quotation_id):
    quotation = get_object_or_404(Quotation, quotation_id=quotation_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="quotation_{quotation.quotation_id}.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 750, f"Quotation ID: {quotation.quotation_id}")
    p.drawString(100, 730, f"Customer: {quotation.customer.name}")
    p.drawString(100, 710, f"Amount Due: {quotation.amount_due}")
    p.drawString(100, 690, f"Status: {quotation.status}")
    p.showPage()
    p.save()
    return response


@login_required(login_url='/auth_app/login/')
def generate_report(request):
    return HttpResponse("Report generated successfully.")
