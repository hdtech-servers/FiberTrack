from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from reportlab.pdfgen import canvas
from .models import Invoice, Quotation, Payment, SubscriptionPlan, CustomItem
from .forms import InvoiceForm, QuotationForm, PaymentForm, SubscriptionPlanForm, CustomItemForm


# Invoice Views
class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'billing/invoice_list.html'
    paginate_by = 10
    login_url = '/authapp/login/'

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'billing/invoice_form.html'
    success_url = reverse_lazy('invoice_list')
    login_url = '/authapp/login/'

class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'billing/invoice_form.html'
    success_url = reverse_lazy('invoice_list')
    login_url = '/authapp/login/'

class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'billing/invoice_confirm_delete.html'
    success_url = reverse_lazy('invoice_list')
    login_url = '/authapp/login/'


# Quotation Views
class QuotationListView(LoginRequiredMixin, ListView):
    model = Quotation
    template_name = 'billing/quotation_list.html'
    paginate_by = 10
    login_url = '/authapp/login/'

class QuotationCreateView(LoginRequiredMixin, CreateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_form.html'
    success_url = reverse_lazy('quotation_list')
    login_url = '/authapp/login/'

class QuotationUpdateView(LoginRequiredMixin, UpdateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_form.html'
    success_url = reverse_lazy('quotation_list')
    login_url = '/authapp/login/'

class QuotationDeleteView(LoginRequiredMixin, DeleteView):
    model = Quotation
    template_name = 'billing/quotation_confirm_delete.html'
    success_url = reverse_lazy('quotation_list')
    login_url = '/authapp/login/'


# Payment Views
class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'billing/payment_list.html'
    paginate_by = 10
    login_url = '/authapp/login/'

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'billing/payment_form.html'
    success_url = reverse_lazy('payment_list')
    login_url = '/authapp/login/'

class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'billing/payment_form.html'
    success_url = reverse_lazy('payment_list')
    login_url = '/authapp/login/'

class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'billing/payment_confirm_delete.html'
    success_url = reverse_lazy('payment_list')
    login_url = '/authapp/login/'


# Subscription Plan Views
class SubscriptionPlanListView(LoginRequiredMixin, ListView):
    model = SubscriptionPlan
    template_name = 'billing/subscription_plan_list.html'
    paginate_by = 10
    login_url = '/authapp/login/'

class SubscriptionPlanCreateView(LoginRequiredMixin, CreateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = 'billing/subscription_plan_form.html'
    success_url = reverse_lazy('subscription_plan_list')
    login_url = '/authapp/login/'

class SubscriptionPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = 'billing/subscription_plan_form.html'
    success_url = reverse_lazy('subscription_plan_list')
    login_url = '/authapp/login/'

class SubscriptionPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = SubscriptionPlan
    template_name = 'billing/subscription_plan_confirm_delete.html'
    success_url = reverse_lazy('subscription_plan_list')
    login_url = '/authapp/login/'


# Custom Item Views
class CustomItemListView(LoginRequiredMixin, ListView):
    model = CustomItem
    template_name = 'billing/custom_item_list.html'
    paginate_by = 10
    login_url = '/authapp/login/'

class CustomItemCreateView(LoginRequiredMixin, CreateView):
    model = CustomItem
    form_class = CustomItemForm
    template_name = 'billing/custom_item_form.html'
    success_url = reverse_lazy('custom_item_list')
    login_url = '/authapp/login/'

class CustomItemUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomItem
    form_class = CustomItemForm
    template_name = 'billing/custom_item_form.html'
    success_url = reverse_lazy('custom_item_list')
    login_url = '/authapp/login/'

class CustomItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomItem
    template_name = 'billing/custom_item_confirm_delete.html'
    success_url = reverse_lazy('custom_item_list')
    login_url = '/authapp/login/'


# PDF Generation Views
@login_required(login_url='/authapp/login/')
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

@login_required(login_url='/authapp/login/')
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
