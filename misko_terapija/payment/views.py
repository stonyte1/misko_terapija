from django.shortcuts import render
from django.conf import settings
from .models import UserPayment
from reservation.models import Client, Reservation
import stripe
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from .models import Client

def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    house_id = int(session.metadata.get('house_id'))
    date_from = session.metadata.get('date_from')
    date_to = session.metadata.get('date_to')
    reservation = Reservation(date_from=date_from, date_to=date_to, house_id=house_id)
    reservation.save()

    customer = stripe.Customer.retrieve(session.customer)
    client_id = request.user.id  # Assuming user_id is the primary key of your User model
    client, created = Client.objects.get_or_create(id=client_id)

    # Update the client's information with the data from the payment
    client.name = customer.name
    client.email = customer.email
    client.phone_number = customer.phone
    client.save()

    return render(request, 'payment/payment_successful.html', {'reservation': reservation, 'client': client})

def payment_cancelled(request):
    return render(request, 'payment/payment_cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as err:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as err:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']
        session_id = session.get('id', None)
        time.sleep(15)
        client_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        client_payment.payment_bool = True
        client_payment.save()
    return HttpResponse(status=200)