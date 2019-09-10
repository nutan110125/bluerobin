import requests
import json
from django.conf import settings


def get_customer():
    response = requests.get(
        'https://api.escrow.com/2017-09-01/customer/me',
        auth=(
            settings.ESCROW_EMAIL,
            settings.ESCROW_KEY
        ),
    )
    responseData = json.loads(response._content.decode("utf-8"))


def create_customer(user):
    response = requests.post(
        'https://api.escrow.com/2017-09-01/customer',
        auth=(
            settings.ESCROW_EMAIL,
            settings.ESCROW_KEY
        ),
        json={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "address": {
                "line1": "1829 West Lane",
                "line2": "Apartment 301020",
                "city": "San Francisco",
                "state": "CA",
                "country": "US",
                "post_code": "10203"
            },
            "phone_number": "8885118600"
        }
    )

    responseData = json.loads(response._content.decode("utf-8"))


def create_transaction():
    response = requests.post(
        'https://api.escrow.com/2017-09-01/transaction',
        auth=(
            settings.ESCROW_EMAIL,
            settings.ESCROW_KEY
        ),
        json={
            "parties": [
                {
                    "role": "buyer",
                    "customer": "me"
                },
                {
                    "role": "seller",
                    "customer": "keanu.reaves@escrow.com"
                }
            ],
            "currency": "usd",
            "description": "The sale of johnwick.com",
            "items": [
                {
                    "title": "johnwick.com",
                    "description": "johnwick.com",
                    "type": "domain_name",
                    "inspection_period": 259200,
                    "quantity": 1,
                    "schedule": [
                        {
                            "amount": 1000.0,
                            "payer_customer": "me",
                            "beneficiary_customer": "keanu.reaves@escrow.com"
                        }
                    ]
                }
            ]
        },
    )
    responseData = json.loads(response._content.decode("utf-8"))
