from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import UserPayment
from reservation.models import Client, Reservation
import stripe
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Client
import random
import requests
from datetime import datetime


def send_email_client(client, reservation):
    email_body = render_to_string('payment/email_client.html', {'reservation': reservation, 'client': client})
    email_message = EmailMultiAlternatives(
        'Apmokėjimas pavyko',
        email_body,
        'admin@misko_terapija.com',  # Sender's email address
        [client.email],  # Client email address
    )
    email_message.content_subtype = 'html'  # Set the content type as HTML
    email_message.send()


def send_email_moderator(client, reservation):
    email_body = render_to_string('payment/email_moderator.html', {'reservation': reservation, 'client': client})
    email_message = EmailMultiAlternatives(
        'Nauja rezervacija',
        email_body,
        'admin@misko_terapija.com',  # Sender's email address
        ['stonyteevelina@gmail.com'],  # Moderator email address
    )
    email_message.content_subtype = 'html'  # Set the content type as HTML
    email_message.send()


def add_calendar(house, date_from, date_to, email):
    url = "https://v1.nocodeapi.com/mermaido_leg/calendar/VVuVsNbfRLlnYKgd/event"

    date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
    date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")
    date_from = date_from_dt.strftime("%Y-%m-%dT%H:%M:%S")
    date_to = date_to_dt.strftime("%Y-%m-%dT%H:%M:%S")

    calendar_data = {
        "summary": "Miško terapija",
        "location": "Žukonys, Varena, Lithuania, 65248",
        "description": f"{house} namuko rezevacija.",
        "start": {
            "dateTime": date_from,
            "timeZone": "Europe/Vilnius"
        },
        "end": {
            "dateTime": date_to,
            "timeZone": "Europe/Vilnius"
        },
        "recurrence": ["RRULE:FREQ=DAILY;COUNT=2"],
        "sendNotifications": True,
        "attendees": [
            {"email": email}, # Reciever
            {"email": "admin@misko_terapija.com"}, #Sender
        ]
    }

    requests.post(url=url, json=calendar_data)


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

    if settings.DEBUG:
        client_id = random.randint(0, 999999999) # Replace with a unique client ID for testing
    else:
        client_id = request.user.id

    client, created = Client.objects.get_or_create(id=client_id)

    # Update the client's information with the data from the payment
    client.name = customer.name
    client.email = customer.email
    client.phone_number = customer.phone
    client.reservation = reservation
    client.save()

    send_email_client(client, reservation)
    send_email_moderator(client, reservation)
    add_calendar(reservation.house, date_from, date_to, client.email)

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