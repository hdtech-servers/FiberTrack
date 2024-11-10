# utils.py

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from settings.models import OrganizationSettings
import base64
import datetime


def get_access_token():
    org_settings = OrganizationSettings.objects.first()
    consumer_key = org_settings.mpesa_consumer_key
    consumer_secret = org_settings.mpesa_consumer_secret
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" if org_settings.mpesa_environment == 'sandbox' else "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    return json_response['access_token']


def initiate_stk_push(invoice):
    org_settings = OrganizationSettings.objects.first()
    access_token = get_access_token()

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" if org_settings.mpesa_environment == 'sandbox' else "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}

    # Prepare the password and timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        f"{org_settings.mpesa_short_code}{org_settings.mpesa_passkey}{timestamp}".encode()).decode('utf-8')

    payload = {
        "BusinessShortCode": org_settings.mpesa_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(invoice.amount_due),  # Amount due on the invoice
        "PartyA": invoice.customer.phone_number,  # Customer phone number
        "PartyB": org_settings.mpesa_short_code,
        "PhoneNumber": invoice.customer.phone_number,
        "CallBackURL": settings.BASE_URL + "/mpesa/callback/",
        "AccountReference": invoice.invoice_id,
        "TransactionDesc": "Invoice Payment"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
