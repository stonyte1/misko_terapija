from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation, House
from .forms import ReservationForm
from datetime import timedelta, datetime
import stripe
from django.conf import settings



def get_price(date_from, date_to, house):
    price = 0
    current_date = date_from
    while current_date <= date_to:
        date_str = current_date.strftime('%Y-%m-%d')
        date = datetime.strptime(date_str, '%Y-%m-%d')
        weekday = date.weekday()
        if weekday == 4 or weekday == 5:
            price += house.price_weekend
        else:
            price += house.price
        current_date += timedelta(days=1)
    return price

    
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

    check_in_date = request.GET.get('check-in')
    check_out_date = request.GET.get('check-out')
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.house = house
            price = get_price(reservation.date_from, reservation.date_to, house)

            # Create the payment session and redirect to the payment page
            stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'eur',
                                'unit_amount': int(price * 100),  # Convert price to cents (Stripe requires the amount in cents)
                                'product_data': {
                                    'name': house.name,  # Set the product name to the house name
                                },
                            },
                            'quantity': 1,

                        }
                    ],
                    mode='payment',
                    allow_promotion_codes = True,
                    customer_creation='always',
                    success_url=settings.REDIRECT_DOMAIN + f'/payment/payment_successful?session_id={{CHECKOUT_SESSION_ID}}',
                    cancel_url=settings.REDIRECT_DOMAIN + '/payment/payment_cancelled',
                    metadata={
                        'house_id': house.id,
                        'date_from': reservation.date_from,
                        'date_to': reservation.date_to
                    }, 
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
        if check_in_date == "None":
            check_in_date = None
        if check_out_date == "None":
            check_out_date = None

    context = {
        'form': form,
        'reserved_dates': reserved_dates,
        'house': house,
        'images': images,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
    }
    return render(request, 'reservation/house_detail.html', context)
