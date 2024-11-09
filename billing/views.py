from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.db.models import Sum, Q
from reportlab.platypus import Table, TableStyle, paragraph
from reportlab.lib.styles import getSampleStyleSheet
from settings.models import OrganizationSettings
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
    login_url = '/auth_app/login/'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search filter
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(customer__first_name__icontains=query) |
                Q(customer__last_name__icontains=query) |
                Q(id__icontains=query)
            )

        # Status filter
        status = self.request.GET.get('status')
        if status and status != 'all':
            queryset = queryset.filter(status=status)

        # Sorting
        sort_by = self.request.GET.get('sort_by', 'id')  # Default sort by 'id'
        sort_order = self.request.GET.get('sort_order', 'asc')
        if sort_order == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['status_filter'] = self.request.GET.get('status', 'all')
        context['sort_by'] = self.request.GET.get('sort_by', 'id')
        context['sort_order'] = self.request.GET.get('sort_order', 'asc')
        return context


# View to select a customer before creating a quotation
class CustomerSelectView(ListView):
    model = Customer
    template_name = 'billing/select_customer.html'
    context_object_name = 'customers'


class QuotationDetailView(View):
    template_name = 'billing/quotation_detail.html'

    def get(self, request, pk):
        quotation = get_object_or_404(Quotation, pk=pk)
        form = QuotationForm(instance=quotation)
        form.fields = {'status'}  # Only include the status field in the form
        return render(request, self.template_name, {
            'quotation': quotation,
            'form': form,
            'items': quotation.items.all(),
        })

    def post(self, request, pk):
        quotation = get_object_or_404(Quotation, pk=pk)
        form = QuotationForm(request.POST, instance=quotation)

        if form.is_valid():
            form.save()
            messages.success(request, "Quotation status updated successfully.")
            return redirect('quotation_detail', pk=pk)
        else:
            messages.error(request, "Failed to update quotation status.")
            return render(request, self.template_name, {
                'quotation': quotation,
                'form': form,
                'items': quotation.items.all(),
            })

class QuotationCreateView(CreateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_form.html'
    success_url = reverse_lazy('quotation_list')

    def dispatch(self, request, *args, **kwargs):
        self.customer = get_object_or_404(Customer, customer_id=kwargs.get('customer_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.customer
        if self.request.POST:
            context['item_formset'] = CustomItemFormSet(self.request.POST, prefix="items")  # Set prefix
        else:
            context['item_formset'] = CustomItemFormSet(prefix="items")  # Set prefix
        return context

    def form_valid(self, form):
        form.instance.customer = self.customer
        response = super().form_valid(form)

        item_formset = CustomItemFormSet(self.request.POST, instance=self.object, prefix="items")  # Use prefix
        if item_formset.is_valid():
            item_formset.save()

            total_amount_due = sum(item.total_price for item in self.object.items.all())
            self.object.amount_due = total_amount_due
            self.object.save()

            messages.success(self.request, "Quotation created successfully.")
            return response
        else:
            print("Item formset is invalid.")
            print(item_formset.errors)  # For debugging
            return self.form_invalid(form)


class QuotationUpdateView(UpdateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_edit.html'
    success_url = reverse_lazy('quotation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = CustomItemFormSet(self.request.POST, instance=self.object)
        else:
            context['item_formset'] = CustomItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']

        # Remove empty forms from the formset before validation
        for item_form in item_formset.forms:
            if not item_form.cleaned_data.get('item_name') and not item_form.cleaned_data.get('price'):
                item_formset.forms.remove(item_form)

        if form.is_valid() and item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()

            # Calculate and update the total amount due
            total_amount_due = sum(item.total_price for item in self.object.items.all())
            self.object.amount_due = total_amount_due
            self.object.save()

            messages.success(self.request, "Quotation updated successfully.")
            return redirect(self.success_url)

        # Print errors for debugging
        if not form.is_valid():
            print("Quotation form errors:", form.errors)
        if not item_formset.is_valid():
            print("Item formset errors:", item_formset.errors)
            for form in item_formset:
                print("Individual item errors:", form.errors)

        messages.error(self.request, "There was an error with your submission. Please correct the errors and try again.")
        return self.form_invalid(form)
class QuotationDeleteView(DeleteView):
    model = Quotation
    template_name = 'billing/quotation_confirm_delete.html'
    success_url = reverse_lazy('quotation_list')  # Adjust based on your app name


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


def generate_quotation_pdf(request, pk):
    # Get quotation data
    quotation = get_object_or_404(Quotation, pk=pk)

    # Try to get organization settings, or set to None
    organization = OrganizationSettings.objects.first()

    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="quotation_{quotation.id}.pdf"'

    # Create the PDF object
    buffer = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Add organization details if available
    if organization:
        buffer.setFont("Helvetica-Bold", 12)
        buffer.drawString(40, height - 40, organization.name or "Organization Name")
        buffer.setFont("Helvetica", 10)
        buffer.drawString(40, height - 60, f"Address: {organization.address or 'N/A'}")
        buffer.drawString(40, height - 75, f"Contact: {organization.contact_number or 'N/A'}")
        buffer.drawString(40, height - 90, f"Email: {organization.email or 'N/A'}")
    else:
        buffer.drawString(40, height - 40, "Organization details not available")

    # Draw quotation information
    buffer.setFont("Helvetica-Bold", 12)
    buffer.drawString(40, height - 130, f"Quotation ID: {quotation.id}")
    buffer.drawString(40, height - 145, f"Customer: {quotation.customer.first_name} {quotation.customer.last_name}")
    buffer.drawString(40, height - 160, f"Amount Due: KSH {quotation.amount_due}")

    # Table for items
    data = [["Item Name", "Description", "Quantity", "Unit", "Price (KSH)", "Total Price (KSH)"]]
    for item in quotation.items.all():
        data.append([
            item.item_name,
            item.item_description,
            item.quantity,
            item.unit,
            f"{item.price:.2f}",
            f"{item.total_price:.2f}"
        ])

    # Create the table with styling
    table = Table(data, colWidths=[1.5 * inch, 2 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Place table in the PDF
    table.wrapOn(buffer, width, height)
    table.drawOn(buffer, 40, height - 300)

    # Finalize and save the PDF
    buffer.showPage()
    buffer.save()
    return response