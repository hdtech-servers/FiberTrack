import json
import logging
import traceback
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.db.models import Sum, Q
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Spacer, Image
from reportlab.platypus.para import Paragraph
from settings.models import OrganizationSettings
from customers.models import Customer
from .models import Invoice, Quotation, Payment, CustomItem
from .forms import InvoiceForm, QuotationForm, PaymentForm, CustomItemForm, CustomItemFormSet
from .utils import initiate_stk_push


# Dashboard View
class BillingDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'billing/dashboard.html'
    login_url = '/auth_app/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total revenue from all payments
        context['total_revenue'] = Payment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0

        # Total outstanding payments for invoices with 'Pending' or 'Overdue' status
        context['outstanding_payments'] = \
        Invoice.objects.filter(status__in=['Pending', 'Overdue']).aggregate(total=Sum('amount_due'))['total'] or 0

        # Count of all invoices
        context['invoice_count'] = Invoice.objects.count()

        # Payments received count
        context['payments_received_count'] = Payment.objects.count()

        # Recent invoices
        context['recent_invoices'] = Invoice.objects.order_by('-due_date')[:5]

        # Recent payments
        context['recent_payments'] = Payment.objects.order_by('-payment_date')[:5]

        # Payment status distribution
        context['paid_count'] = Invoice.objects.filter(status='Paid').count()
        context['pending_count'] = Invoice.objects.filter(status='Pending').count()
        context['overdue_count'] = Invoice.objects.filter(status='Overdue').count()

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
    success_url = reverse_lazy('billing:invoice_list')
    login_url = '/auth_app/login/'

    def get_object(self, queryset=None):
        return get_object_or_404(Invoice, invoice_id=self.kwargs.get('invoice_id'))


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'billing/invoice_confirm_delete.html'
    success_url = reverse_lazy('billing:invoice_list')
    login_url = '/auth_app/login/'

    def get_object(self, queryset=None):
        return get_object_or_404(Invoice, invoice_id=self.kwargs.get('invoice_id'))


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



class InvoiceDetailView(View):
    template_name = 'billing/invoice_detail.html'

    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
        form = InvoiceForm(instance=invoice)
        form.fields = {'status'}  # Limit fields if necessary
        return render(request, self.template_name, {
            'invoice': invoice,
            'form': form,
            'items': invoice.items.all(),
        })

    def post(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
        form = InvoiceForm(request.POST, instance=invoice)

        if form.is_valid():
            form.save()
            messages.success(request, "Invoice status updated successfully.")
            return redirect('invoice_detail', invoice_id=invoice_id)
        else:
            messages.error(request, "Failed to update invoice status.")
            return render(request, self.template_name, {
                'invoice': invoice,
                'form': form,
                'items': invoice.items.all(),
            })


# Quotation Views with Custom Item Inline Support
class QuotationListView(LoginRequiredMixin, ListView):
    model = Quotation
    template_name = 'billing/quotation_list.html'
    login_url = '/auth_app/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(customer__first_name__icontains=query) |
                Q(customer__last_name__icontains=query) |
                Q(id__icontains=query)
            )

        status = self.request.GET.get('status')
        if status and status != 'all':
            queryset = queryset.filter(status=status)

        sort_by = self.request.GET.get('sort_by', 'id')
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


class CustomerSelectView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'billing/select_customer.html'
    context_object_name = 'customers'
    login_url = '/auth_app/login/'


class QuotationDetailView(LoginRequiredMixin, View):
    template_name = 'billing/quotation_detail.html'
    login_url = '/auth_app/login/'

    def get(self, request, quotation_id):
        quotation = get_object_or_404(Quotation, quotation_id=quotation_id)
        form = QuotationForm(instance=quotation)
        form.fields = {'status'}
        return render(request, self.template_name, {
            'quotation': quotation,
            'form': form,
            'items': quotation.items.all(),
        })

    def post(self, request, quotation_id):
        quotation = get_object_or_404(Quotation, quotation_id=quotation_id)
        form = QuotationForm(request.POST, instance=quotation)

        if form.is_valid():
            form.save()
            messages.success(request, "Quotation status updated successfully.")
            return redirect('quotation_detail', quotation_id=quotation_id)
        else:
            messages.error(request, "Failed to update quotation status.")
            return render(request, self.template_name, {
                'quotation': quotation,
                'form': form,
                'items': quotation.items.all(),
            })


class QuotationCreateView(LoginRequiredMixin, CreateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_form.html'
    success_url = reverse_lazy('quotation_list')
    login_url = '/auth_app/login/'

    def dispatch(self, request, *args, **kwargs):
        self.customer = get_object_or_404(Customer, customer_id=kwargs.get('customer_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.customer
        if self.request.POST:
            context['item_formset'] = CustomItemFormSet(self.request.POST, prefix="items")
        else:
            context['item_formset'] = CustomItemFormSet(prefix="items")
        return context

    def form_valid(self, form):
        form.instance.customer = self.customer
        response = super().form_valid(form)

        item_formset = CustomItemFormSet(self.request.POST, instance=self.object, prefix="items")
        if item_formset.is_valid():
            item_formset.save()
            total_amount_due = sum(item.total_price for item in self.object.items.all())
            self.object.amount_due = total_amount_due
            self.object.save()
            messages.success(self.request, "Quotation created successfully.")
            return response
        else:
            print("Item formset is invalid.")
            print(item_formset.errors)
            return self.form_invalid(form)


class QuotationUpdateView(LoginRequiredMixin, UpdateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'billing/quotation_edit.html'
    success_url = reverse_lazy('quotation_list')
    login_url = '/auth_app/login/'

    def get_object(self, queryset=None):
        return get_object_or_404(Quotation, quotation_id=self.kwargs.get('quotation_id'))

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

        for item_form in item_formset.forms:
            if not item_form.cleaned_data.get('item_name') and not item_form.cleaned_data.get('price'):
                item_formset.forms.remove(item_form)

        if form.is_valid() and item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()
            total_amount_due = sum(item.total_price for item in self.object.items.all())
            self.object.amount_due = total_amount_due
            self.object.save()
            messages.success(self.request, "Quotation updated successfully.")
            return redirect(self.success_url)

        if not form.is_valid():
            print("Quotation form errors:", form.errors)
        if not item_formset.is_valid():
            print("Item formset errors:", item_formset.errors)
            for form in item_formset:
                print("Individual item errors:", form.errors)

        messages.error(self.request, "There was an error with your submission. Please correct the errors and try again.")
        return self.form_invalid(form)


class QuotationDeleteView(LoginRequiredMixin, DeleteView):
    model = Quotation
    template_name = 'billing/quotation_confirm_delete.html'
    success_url = reverse_lazy('quotation_list')
    login_url = '/auth_app/login/'

    def get_object(self, queryset=None):
        return get_object_or_404(Quotation, quotation_id=self.kwargs.get('quotation_id'))


@login_required(login_url='/auth_app/login/')
def generate_quotation_pdf(request, quotation_id):
    # Fetch data
    quotation = get_object_or_404(Quotation, quotation_id=quotation_id)
    organization = OrganizationSettings.objects.first()

    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="quotation_{quotation.quotation_id}.pdf"'

    # Define the document
    buffer = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    bold_style = styles["Heading3"]

    # Elements for the PDF
    elements = []

    # Add header with logo and organization details
    header_data = [
        [
            Paragraph(f"<b>{organization.name or 'Organization Name'}</b>", bold_style),
            Image(organization.logo.path, width=1.5 * inch, height=0.75 * inch) if organization and organization.logo else ""
        ],
        [
            Paragraph(organization.address or "Address not available", normal_style),
            ""
        ],
        [
            Paragraph(f"Contact: {organization.contact_number or 'N/A'}", normal_style),
            ""
        ],
        [
            Paragraph(f"Email: {organization.email or 'N/A'}", normal_style),
            ""
        ]
    ]

    header_table = Table(header_data, colWidths=[4.5 * inch, 2 * inch])
    elements.append(header_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Quotation Number and Customer Details aligned beneath logo and organization
    number_customer_data = [
        [Paragraph(f"<b>Quotation #{quotation.quotation_id}</b>", normal_style), ""],
        ["", ""],
        [
            Paragraph(f"<b>Customer:</b>", normal_style),
            Paragraph(f"{quotation.customer.first_name} {quotation.customer.last_name}", normal_style)
        ],
        [
            "",
            Paragraph(quotation.customer.billing_address or "Billing address not available", normal_style)
        ]
    ]
    number_customer_table = Table(number_customer_data, colWidths=[4.5 * inch, 2 * inch])
    elements.append(number_customer_table)
    elements.append(Spacer(1, 0.5 * inch))

    # Table for Items
    item_data = [["ITEM", "DESCRIPTION", "QTY", "UNIT", "PRICE", "TOTAL"]]
    for item in quotation.items.all():
        item_data.append([item.item_name, item.item_description, item.quantity, item.unit,
                          f"KES {item.price:.2f}", f"KES {item.total_price:.2f}"])
    item_data.append(["", "", "", "", "SUBTOTAL", f"KES {quotation.amount_due:.2f}"])
    item_data.append(["", "", "", "", "TOTAL", f"KES {quotation.amount_due:.2f}"])

    # Styling for item table
    item_table = Table(item_data, colWidths=[1.5 * inch, 2.5 * inch, 0.6 * inch, 0.6 * inch, 1.2 * inch, 1.2 * inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
    ]))
    elements.append(item_table)
    elements.append(Spacer(1, 0.5 * inch))

    # Notes Section as plain text
    note_text = organization.quote_notes or "Note: Terms and conditions apply."
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"<b>NOTE:</b> {note_text}", normal_style))

    # Build the PDF with elements
    buffer.build(elements)
    return response


# Initialize logger
logger = logging.getLogger(__name__)

@login_required(login_url='/auth_app/login/')
def send_quotation_email_view(request, quotation_id):
    # Fetch the quotation using quotation_id
    quotation = get_object_or_404(Quotation, quotation_id=quotation_id)
    try:
        send_quotation_email(quotation_id)  # Call send_quotation_email without request
        messages.success(request, f"Quotation email sent successfully to {quotation.customer.email}.")
    except Exception as e:
        # Log error details for debugging
        logger.error("Failed to send email", exc_info=True)
        messages.error(request, f"Failed to send email: {str(e)}")
    return redirect('quotation_list')

def send_quotation_email(quotation_id):
    try:
        # Retrieve the specified quotation
        quotation = Quotation.objects.get(quotation_id=quotation_id)
        organization_settings = OrganizationSettings.objects.first()

        if not organization_settings:
            raise ValueError("Organization settings are missing")

        # Set up email configuration from organization settings
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        settings.EMAIL_HOST = organization_settings.smtp_host
        settings.EMAIL_PORT = organization_settings.smtp_port
        settings.EMAIL_HOST_USER = organization_settings.smtp_username
        settings.EMAIL_HOST_PASSWORD = organization_settings.smtp_password
        settings.EMAIL_USE_TLS = organization_settings.smtp_use_tls
        settings.EMAIL_USE_SSL = organization_settings.smtp_use_ssl

        # Prepare email details
        recipient_email = quotation.customer.email
        subject = f"New Quotation: {quotation.quotation_id}"
        message = f"Dear {quotation.customer.first_name},\n\nPlease find attached your quotation.\n\nBest regards,\n{organization_settings.name or 'Your Company'}"
        from_email = organization_settings.smtp_from_email or settings.DEFAULT_FROM_EMAIL

        # Send the email
        send_mail(
            subject,
            message,
            from_email,
            [recipient_email],
            fail_silently=False,
        )
    except Exception as e:
        # Log error details for debugging
        logger.error("Error in send_quotation_email function", exc_info=True)
        print(f"Error sending email: {e}")
        raise  # Re-raise the exception to be caught in the view


@login_required(login_url='/auth_app/login/')
def initiate_payment_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    response = initiate_stk_push(invoice)

    if response.get('ResponseCode') == '0':
        return JsonResponse({'success': True, 'message': 'STK Push initiated successfully',
                             'CheckoutRequestID': response['CheckoutRequestID']})
    else:
        return JsonResponse({'success': False, 'message': 'Failed to initiate STK Push', 'error': response})


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    result_code = data['Body']['stkCallback']['ResultCode']

    if result_code == 0:
        callback_metadata = data['Body']['stkCallback']['CallbackMetadata']['Item']
        transaction_id = [item['Value'] for item in callback_metadata if item['Name'] == 'MpesaReceiptNumber'][0]
        phone_number = [item['Value'] for item in callback_metadata if item['Name'] == 'PhoneNumber'][0]
        amount_paid = [item['Value'] for item in callback_metadata if item['Name'] == 'Amount'][0]
        invoice_id = data['Body']['stkCallback']['MerchantRequestID']  # Use this to link to the invoice

        # Process payment
        invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
        Payment.objects.create(
            invoice=invoice,
            payment_method="Mpesa",
            transaction_id=transaction_id,
            amount_paid=amount_paid,
            processed_by=request.user
        )

        # Update invoice status if paid in full
        if amount_paid >= invoice.amount_due:
            invoice.status = 'Paid'
            invoice.save()

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})