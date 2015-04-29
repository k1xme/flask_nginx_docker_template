import os
import paypalrestsdk

# Initialized Paypal RESTful client.
PAYPAL_CLIENT_ID = 'AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd'
PAYPAL_CLIENT_SECRET = 'EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX'
PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')
PAYPAL_RETURN_URL = "http://localhost:4567/approve-payment?success=true"
PAYPAL_CANCEL_URL = "http://localhost:4567/approve-payment?success=false"
PAYMENT_SERVER_SECRET_KEY = os.environ.get('PAYMENT_SERVER_SECRET_KEY', "doushidashabi")
PAYMENT_SERVER_PORT = os.environ.get('PAYMENT_SERVER_PORT', 5000)
ACCESS_CHECKING_URL = '/check-access.html'
CREATE_PAYMENT_URL = 'create-payment.html'
CREATE_FAILED_URL = CREATE_PAYMENT_URL
# Payment status
APPROVED = 'approved'
PAYMENT_DESC = 'Recharge Fee'
APPROVE_PAYMENT_FAILED_URL = "/success.html"
APPROVE_PAYMENT_SUCCESS_URL = "/failure.html"
ACCESS_CODE_PATTERN = r"k.{3}s.{3}"

#-----------------------------------------------------------------------------
# Initialization Function

paypal_api = paypalrestsdk.configure({
    'mode': PAYPAL_MODE,
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET})

def create_payment(payment_amount):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
        "return_url": PAYPAL_RETURN_URL,
        "cancel_url": PAYPAL_CANCEL_URL},
        "transactions": [{
        "amount": {"total": str(payment_amount), "currency": "USD"},
        "description": PAYMENT_DESC}]})

    if payment.create():
        print payment.links
    else:
        print payment.error
