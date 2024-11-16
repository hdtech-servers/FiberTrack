from django.urls import path
from . import views
from .views import (
    InvoiceListView, InvoiceCreateView, InvoiceUpdateView, InvoiceDeleteView, generate_invoice_pdf,
    QuotationListView, QuotationCreateView, QuotationUpdateView, QuotationDeleteView,
    BillingDashboardView, CustomerSelectView, QuotationDetailView, mpesa_callback, payment_list,
    initiate_stk_push_from_customer_detail,
)

urlpatterns = [
    # Dashboard URL
    path('', BillingDashboardView.as_view(), name='billing_dashboard'),

    # Invoice URLs
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/<int:invoice_id>/update/', InvoiceUpdateView.as_view(), name='invoice_update'),
    path('invoices/<int:invoice_id>/delete/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoices/<int:invoice_id>/pdf/', generate_invoice_pdf, name='invoice_pdf'),

    # Quotation URLs
    path('quotations/', QuotationListView.as_view(), name='quotation_list'),
    path('quotations/select_customer/', CustomerSelectView.as_view(), name='select_customer'),
    path('quotations/create/<str:customer_id>/', QuotationCreateView.as_view(), name='create_quotation'),
    path('quotations/<str:quotation_id>/', QuotationDetailView.as_view(), name='quotation_detail'),
    path('quotations/<str:quotation_id>/edit/', QuotationUpdateView.as_view(), name='quotation_update'),
    path('quotations/<str:quotation_id>/delete/', QuotationDeleteView.as_view(), name='quotation_delete'),
    path('quotations/<str:quotation_id>/pdf/', views.generate_quotation_pdf, name='quotation_pdf'),
    path('send-quotation-email/<str:quotation_id>/', views.send_quotation_email_view, name='send_quotation_email'),

    path('mpesa_callback/', mpesa_callback, name='mpesa_callback'),
    path('customer/<str:customer_id>/stk_push/', initiate_stk_push_from_customer_detail, name='initiate_stk_push'),
    path('payments/', payment_list, name='payment_list'),
]
