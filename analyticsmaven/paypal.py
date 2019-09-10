import collections
import requests
import json
# hdassosiation-facilitator@gmail.com
from django.contrib.sites.shortcuts import get_current_site

from .models import AppliedJobs, TransactionManagement

keys = json.load(open("bluerobins/credentials.json"))
headers = {
    # The first three are from my developer account
    "X-PAYPAL-SECURITY-USERID": keys["user_id"],
    "X-PAYPAL-SECURITY-PASSWORD": keys["password"],
    "X-PAYPAL-SECURITY-SIGNATURE": keys["signature"],
    "X-PAYPAL-APPLICATION-ID": "APP-80W284485P519543T",
    "X-PAYPAL-SERVICE-VERSION": "1.1.0",
    "X-PAYPAL-REQUEST-DATA-FORMAT": "JSON",
    "X-PAYPAL-RESPONSE-DATA-FORMAT": "JSON"
}


def payment(request, job, amount, type):
    applied_job = AppliedJobs.objects.get(id=job)
    if type == "Advance":
        receiver = [
            {
                "amount": str(int(float(amount)-(float(amount)*10)/100)),
                "email": "rishabhsiet0065@gmail.com"
            },
            {
                "amount": str(int((float(amount)*10)/100)),
                "email": applied_job.user.paypal_email if applied_job.user.paypal_email else applied_job.user.email
            }
        ]
        returnURL = "{}/paypal-payment-advance/{}".format(
            "http://"+str(get_current_site(request)), job)
        cancelURL = "{}/my-jobs".format(
            "http://"+str(get_current_site(request)))
        payment_type = "ADVANCE"
        released = True

    else:
        receiver = [
            {
                "amount": str(int(float(amount))),
                "email": "rishabhsiet0065@gmail.com"
            }
        ]
        returnURL = "{}/paypal-payment-escrow/{}".format(
            "http://"+str(get_current_site(request)), job)
        cancelURL = "{}/job-approval/{}/{}".format(
            "http://"+str(get_current_site(request)), applied_job.user.uuid, applied_job.uuid)
        payment_type = "ESCROW"
        released = False
    params = collections.OrderedDict()
    params = {
        "actionType": "PAY",  # Specify the Payment Action
        "currencyCode": "USD",  # Specify the Country Code
        "receiverList": {
            "receiver": receiver
        },  # The payment Receiver's Email Address

        # Where the Sender is redirected to after approving a successful payment
        "returnUrl": returnURL,
        # Where the Sender is redirected to upon a canceled payment
        "cancelUrl": cancelURL,
        "requestEnvelope": {
            "errorLanguage": "en_US",
            "detailLevel": "ReturnAll"
        }
    }

    # Send a Pay request to PayPal
    url = "https://svcs.sandbox.paypal.com/AdaptivePayments/Pay"
    response = requests.post(url, data=json.dumps(params), headers=headers)

    # Check the response:
    print(response.content.decode())
    response_string = response.content.decode("utf-8")
    response_dict = json.loads(response_string)
    key = response_dict.get("payKey")
    if response_dict['responseEnvelope']['ack'] == 'Success':
        transaction, created = TransactionManagement.objects.get_or_create(
            recipient=applied_job.user,
            sender=applied_job.job.company_name.user,
            job=applied_job,
            recipient_share=int(float(amount) - (float(amount)*10)/100),
            analytics_share=int((float(amount)*10)/100),
            key=key,
            payment=payment_type,
            total=float(amount),
            released=released
        )
        data = {}
        data['ack'] = response_dict['responseEnvelope']['ack']
        data['url'] = "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey=" + key
        return data
    else:
        print("Failure Response")
        return response_dict


def paypal_transaction_details(key):
    url = "https://svcs.sandbox.paypal.com/AdaptivePayments/PaymentDetails"
    params = collections.OrderedDict()
    params = {
        "payKey": key,
        "requestEnvelope": {
            "errorLanguage": "en_US",
            "detailLevel": "ReturnAll"   # Error detail level
        }}
    response = requests.post(url, data=json.dumps(params), headers=headers)
    return response.content
