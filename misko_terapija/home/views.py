from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import House
from reservation.forms import ReservationForm
from reservation.views import get_reserved_dates
import stripe
from django.conf import settings


def reservation_create(request, pk):
    house = get_object_or_404(House, pk=pk)
    reserved_dates = get_reserved_dates()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.house = house

            # Get the house price
            house_price = house.price  # Assuming the price is stored in the 'price' field of the House model

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
                            'quantity': 1,
                        }
                    ],
                    mode='payment',
                    customer_creation='always',
                    success_url=settings.REDIRECT_DOMAIN + f'/payment/product_page?session_id={{CHECKOUT_SESSION_ID}}',
                    cancel_url=settings.REDIRECT_DOMAIN + '/payment/payment_cancelled',
                    metadata={
                        'reservation_id': reservation.id  # Pass the reservation ID as metadata
                    }
                )
                reservation.save()
                return redirect(checkout_session.url, code=303)
            except stripe.error.StripeError as e:
                # Handle any Stripe errors
                print(e)
                return redirect('payment_error')  # Replace 'payment_error' with the appropriate error handling view or URL
        else:
            print(form.errors)
    else:
        form = ReservationForm(initial={'house': house})

    context = {
        'form': form,
        'reserved_dates': reserved_dates,
        'house': house,
    }
    return render(request, 'home/house_detail.html', context)


class HouseListView(generic.ListView):
    model = House
    template_name = "home/home.html"
    context_object_name = 'houses'



