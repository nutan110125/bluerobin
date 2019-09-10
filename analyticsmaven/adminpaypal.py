import random
import string

from paypalrestsdk import Payout, ResourceNotFound

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "EBWKjlELKMYqRNQ6sYvFo64FtaRLRR5BdHEESmha49TM",
    "client_secret": "EO422dn3gQLgDbuwqTjzrFgFtaRLRR5BdHEESmha49TM"})

sender_batch_id = ''.join(
    random.choice(string.ascii_uppercase) for i in range(12))


def adminrelease(transaction)
    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": sender_batch_id,
            "email_subject": "You have a payment"
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": transaction.recipient_share,
                    "currency": "USD"
                },
                "receiver": transaction.recipient.paypal_email,
                "note": "Thank you.",
                "sender_item_id": "item_1"
            }
        ]
    })
    if payout.create():
        print("payout[%s] created successfully" %
              (payout.batch_header.payout_batch_id))
        transaction.released = True
        transaction.save()
    else:
        print(payout.error)
    return
