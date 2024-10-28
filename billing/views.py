import json

from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice, Payment
from .forms import PaymentForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import MpesaService

# List invoices
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    return render(request, 'billing/invoice_list.html', {'invoices': invoices})

# Invoice details
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    payments = Payment.objects.filter(invoice=invoice)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice, 'payments': payments})

# Add payment
def add_payment(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()
            messages.success(request, 'Payment added successfully.')
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = PaymentForm()

    return render(request, 'billing/add_payment.html', {'form': form, 'invoice': invoice})


@csrf_exempt
def mpesa_payment_callback(request):
    if request.method == 'POST':
        mpesa_service = MpesaService()
        data = json.loads(request.body)

        # Process the payment notification
        result = mpesa_service.handle_incoming_payment(data)

        # Send back the result to Mpesa or your internal logs
        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request"}, status=400)
