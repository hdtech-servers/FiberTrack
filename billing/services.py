import requests
from requests.auth import HTTPBasicAuth
import json
from .models import Invoice, Payment
from customer.models import Customer
from settings.models import OrganizationSettings

class MpesaService:

    def __init__(self):
        self.settings = OrganizationSettings.objects.first()
        self.base_url = "https://sandbox.safaricom.co.ke" if self.settings.mpesa_api_mode == "Sandbox" else "https://api.safaricom.co.ke"
        self.consumer_key = self.settings.mpesa_consumer_key
        self.consumer_secret = self.settings.mpesa_consumer_secret
        self.shortcode = self.settings.mpesa_paybill_shortcode
        self.passkey = self.settings.mpesa_passkey
        self.callback_url = self.settings.mpesa_callback_url

    def authenticate(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        mpesa_access_token = json.loads(response.text).get('access_token')
        return mpesa_access_token

    def handle_incoming_payment(self, data):
        """
        Processes incoming payment notification from Mpesa. The data should contain
        customer details, amount, account number (which is the Customer ID), and more.
        """
        # Extract the necessary fields from the response data
        customer_id = data.get('BillRefNumber')
        amount = data.get('TransAmount')
        transaction_id = data.get('TransID')

        try:
            # Ensure the customer ID exists in your system
            customer = Customer.objects.get(customer_id=customer_id)

            # Check if there's an outstanding invoice for this customer
            invoice = Invoice.objects.filter(customer=customer, status='Pending').first()
            if not invoice:
                return {"success": False, "message": "No pending invoices found for this customer."}

            # If the payment is valid, create a Payment record
            Payment.objects.create(
                invoice=invoice,
                payment_method='Mpesa',
                transaction_id=transaction_id,
                amount_paid=amount,
                processed_by=None  # Could be auto-processed
            )

            # Update the invoice status
            invoice.status = 'Paid'
            invoice.save()

            return {"success": True, "message": "Payment successfully processed."}

        except Customer.DoesNotExist:
            return {"success": False, "message": "Customer not found."}
