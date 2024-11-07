from django.urls import path
from .views import (
    InvoiceListView, InvoiceCreateView, InvoiceUpdateView, InvoiceDeleteView, generate_invoice_pdf,
    QuotationListView, QuotationCreateView, QuotationUpdateView, QuotationDeleteView, generate_quotation_pdf,
    PaymentListView, PaymentCreateView, PaymentUpdateView, PaymentDeleteView,
    CustomItemListView, CustomItemCreateView, CustomItemUpdateView, CustomItemDeleteView, BillingDashboardView,
    generate_report, CustomerSelectView, QuotationDetailView
)


urlpatterns = [
    # Dashboard URL
    path('', BillingDashboardView.as_view(), name='billing_dashboard'),

    # Invoice URLs
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<str:invoice_id>/update/', InvoiceUpdateView.as_view(), name='invoice_update'),
    path('invoices/<str:invoice_id>/delete/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoices/<str:invoice_id>/pdf/', generate_invoice_pdf, name='invoice_pdf'),

    # Quotation URLs
    path('quotations/', QuotationListView.as_view(), name='quotation_list'),
    path('quotations/select_customer/', CustomerSelectView.as_view(), name='select_customer'),
    path('quotations/create/<int:customer_id>/', QuotationCreateView.as_view(), name='create_quotation'),  # Only this URL for creating a quotation
    path('quotations/<int:pk>/', QuotationDetailView.as_view(), name='quotation_detail'),
    path('quotations/<int:pk>/edit/', QuotationUpdateView.as_view(), name='quotation_update'),
    path('quotations/<str:quotation_id>/delete/', QuotationDeleteView.as_view(), name='quotation_delete'),
    path('quotations/<str:quotation_id>/pdf/', generate_quotation_pdf, name='quotation_pdf'),

    # Payment URLs
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('payments/<str:payment_id>/update/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/<str:payment_id>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),

    # Custom Item URLs
    path('custom-items/', CustomItemListView.as_view(), name='custom_item_list'),
    path('custom-items/create/', CustomItemCreateView.as_view(), name='custom_item_create'),
    path('custom-items/<str:pk>/update/', CustomItemUpdateView.as_view(), name='custom_item_update'),
    path('custom-items/<str:pk>/delete/', CustomItemDeleteView.as_view(), name='custom_item_delete'),

    # Report Generation URL
    path('generate-report/', generate_report, name='generate_report'),
]
