from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Reservation, House
from .forms import ReservationForm
from datetime import timedelta, date
import stripe
from django.conf import settings
from collections import Counter


def get_reserved_dates(pk):
    reservations = Reservation.objects.filter(house_id=pk)
    reserved_dates = []
    for reservation in reservations:
        current_date = reservation.date_from
        while current_date <= reservation.date_to:
            reserved_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
    return reserved_dates

def reservation_create(request, pk):
    house = get_object_or_404(House, pk=pk)
    reserved_dates = get_reserved_dates(pk)
    images = house.images.all()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.house = house
            quantity = (reservation.date_to - reservation.date_from).days

            # Create the payment session and redirect to the payment page
            stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'eur',
                                'unit_amount': int(house.price * 100),  # Convert price to cents (Stripe requires the amount in cents)
                                'product_data': {
                                    'name': house.name,  # Set the product name to the house name
                                },
                            },
                            'quantity': quantity,
                        }
                    ],
                    mode='payment',
                    customer_creation='always',
                    success_url=settings.REDIRECT_DOMAIN + f'/payment/payment_successful?session_id={{CHECKOUT_SESSION_ID}}',
                    cancel_url=settings.REDIRECT_DOMAIN + '/payment/payment_cancelled',
                    metadata={
                        'house_id': house.id,
                        'date_from': reservation.date_from,
                        'date_to': reservation.date_to
                    }
                )
                return redirect(checkout_session.url, code=303)
            except stripe.error.StripeError as e:
                # Handle any Stripe errors
                print(e)
                return redirect('payment_cancelled')  # Replace 'payment_error' with the appropriate error handling view or URL
        else:
            print(form.errors)

    else:
        form = ReservationForm(initial={'house': house})

    context = {
        'form': form,
        'reserved_dates': reserved_dates,
        'house': house,
        'images': images
    }
    return render(request, 'reservation/house_detail.html', context)

def get_all_reserved_date(houses):
    all_reserved_dates = []
    for house in houses:
        reserved_dates = get_reserved_dates(house.id)
        all_reserved_dates.extend(reserved_dates)
    all_house_reserved = [item for item, count in Counter(all_reserved_dates).items() if count > 1]

    return all_house_reserved

def reservation_filter(request):
    houses = House.objects.all()
    reserved_dates = get_all_reserved_date(houses)
    available_houses = None
    
    if request.method == 'POST':
        check_in_date = request.POST.get('check-in')
        check_out_date = request.POST.get('check-out')
        available_houses = []

        if check_in_date and check_out_date:
            for house in houses:
                booked_dates = get_reserved_dates(house.id)
                is_available = True
                for date in booked_dates:
                    if check_in_date <= date <= check_out_date:
                        is_available = False
                        break

                if is_available:
                    available_houses.append(house)

    context = {
        'reserved_dates': reserved_dates,
        'houses': houses,
        'available_houses': available_houses,
    }
    return render(request, 'reservation/reservation.html', context)
