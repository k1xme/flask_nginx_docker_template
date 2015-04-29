import os
import re
from flask import Flask,redirect, request
import paypalrestsdk

# Initialized Paypal RESTful client.
PAYPAL_CLIENT_ID = 'AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd'
PAYPAL_CLIENT_SECRET = 'EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX'
PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')
PAYPAL_RETURN_URL = "http://192.168.59.103:8080/approve-payment?success=true"
PAYPAL_CANCEL_URL = "http://192.168.59.103:8080/approve-payment?success=false"
PAYMENT_SERVER_SECRET_KEY = os.environ.get('PAYMENT_SERVER_SECRET_KEY', "doushidashabi")
PAYMENT_SERVER_PORT = os.environ.get('PAYMENT_SERVER_PORT', 5000)
ACCESS_CHECKING_URL = 'http://192.168.59.103:8080/check-code.html'
CREATE_PAYMENT_URL = '/create-payment.html'
CREATE_FAILED_URL = CREATE_PAYMENT_URL

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


# Initialized Flask App.
app = Flask(__name__)
app.secret_key = PAYMENT_SERVER_SECRET_KEY

access_code_pattern = re.compile(ACCESS_CODE_PATTERN)

#-----------------------------------------------------------------------------
# ROUTING RULES
@app.route('/create-payment', methods=['POST', 'GET'])
def create_payment():
    if PAYPAL_MODE != 'sandbox': 
        try:
            if not session['pass']:
                return redirect(ACCESS_CHECKING_URL)
        except Exception, e:
            return redirect(ACCESS_CHECKING_URL)

    if request.method == 'GET':
        return redirect(CREATE_PAYMENT_URL)

    redirect_url = CREATE_FAILED_URL

    payment_amount = request.form['payment_amount']

    # Return to this page if the input is not a valid number.
    try:
        float(payment_amount)
    except ValueError as e:
        print e
        return redirect ('/create-payment/')

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
        "return_url": PAYPAL_RETURN_URL,
        "cancel_url": PAYPAL_CANCEL_URL},
        "transactions": [{
        "amount": {"total": payment_amount, "currency": "USD"},
        "description": PAYMENT_DESC}]})

    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))

        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
                break
    else:
        print("Error while creating payment:")
        print(payment.error)

    return redirect(redirect_url)


@app.route('/approve-payment', methods=['GET'])
def approve_payment():
    payment_id = request.args.get('payment_id', None)
    payer_id = request.args.get('payer_id', None)

    if not payer_id or not payment_id:
        return redirect(APPROVE_PAYMENT_FAILED_URL)

    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({"payer_id": payer_id}):
        print("Payment[%s] execute successfully" % (payment.id))
        return redirect(APPROVE_PAYMENT_SUCCESS_URL)

    return redirect(APPROVE_PAYMENT_FAILED_URL)


@app.route('/check-access', methods=['POST'])
def check_access():
    # add hash token to session
    crc = request.form['crc']

    rst = re.match(access_code_pattern, crc)
    
    if not rst:
        return redirect(ACCESS_CHECKING_URL)
    
    session['pass'] = True

    return redirect('/create-payment')

#-----------------------------------------------------------------------------
# Only for debugging
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(PAYMENT_SERVER_PORT)
    app.run(host='0.0.0.0', port=port, debug=True)