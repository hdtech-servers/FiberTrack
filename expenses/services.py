import requests
import base64
import logging
from django.core.cache import cache
from settings.models import OrganizationSettings

logger = logging.getLogger(__name__)

class MPesaService:
    @staticmethod
    def get_organization_settings():
        org_settings = OrganizationSettings.objects.first()
        if not org_settings:
            raise Exception("Organization settings are missing.")
        return org_settings

    @staticmethod
    def get_access_token():
        """Fetch and cache the M-Pesa access token."""
        token = cache.get("mpesa_access_token")
        if token:
            return token

        settings = MPesaService.get_organization_settings()
        consumer_key = settings.mpesa_consumer_key
        consumer_secret = settings.mpesa_consumer_secret

        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" \
            if settings.mpesa_environment == "sandbox" \
            else "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        try:
            response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
            response.raise_for_status()
            token = response.json().get("access_token")
            cache.set("mpesa_access_token", token, timeout=3600)
            return token
        except requests.RequestException as e:
            logger.error(f"Error fetching M-Pesa token: {e}")
            raise Exception("Failed to fetch M-Pesa access token.")

    @staticmethod
    def initiate_b2c_payment(phone_number, amount, reference):
        """Initiates a B2C payment using M-Pesa."""
        settings = MPesaService.get_organization_settings()
        access_token = MPesaService.get_access_token()

        api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest" \
            if settings.mpesa_environment == "sandbox" \
            else "https://api.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"

        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "InitiatorName": settings.mpesa_b2c_initiator_name,
            "SecurityCredential": settings.mpesa_b2c_security_credential,
            "CommandID": settings.mpesa_b2c_command_id,
            "Amount": amount,
            "PartyA": settings.mpesa_b2c_short_code,
            "PartyB": phone_number,
            "Remarks": reference,
            "QueueTimeOutURL": settings.get_b2c_timeout_url(),
            "ResultURL": settings.get_b2c_result_url(),
            "Occasion": reference,
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"B2C Payment initiated successfully: {response.json()}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error initiating B2C payment: {e}")
            raise Exception("Failed to initiate B2C payment.")

    @staticmethod
    def initiate_b2b_payment(shortcode, amount, account_reference):
        """Initiates a B2B payment using M-Pesa."""
        settings = MPesaService.get_organization_settings()
        access_token = MPesaService.get_access_token()

        api_url = "https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest" \
            if settings.mpesa_environment == "sandbox" \
            else "https://api.safaricom.co.ke/mpesa/b2b/v1/paymentrequest"

        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "Initiator": settings.mpesa_b2b_initiator_name,
            "SecurityCredential": settings.mpesa_b2b_security_credential,
            "CommandID": settings.mpesa_b2b_command_id,
            "Amount": amount,
            "PartyA": settings.mpesa_b2b_short_code,
            "PartyB": shortcode,
            "Remarks": account_reference,
            "QueueTimeOutURL": settings.get_b2b_timeout_url(),
            "ResultURL": settings.get_b2b_result_url(),
            "AccountReference": account_reference,
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"B2B Payment initiated successfully: {response.json()}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error initiating B2B payment: {e}")
            raise Exception("Failed to initiate B2B payment.")
