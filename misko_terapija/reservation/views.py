from django.shortcuts import render, redirect
from .models import Reservation, House
from datetime import timedelta
from .forms import ReservationForm, ClientForm


def get_reserved_dates():
    reservations = Reservation.objects.all()
    reserved_dates = []
    for reservation in reservations:
        current_date = reservation.date_from
        while current_date <= reservation.date_to:
            reserved_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
    return reserved_dates


def reservation(request):
    houses = House.objects.all()
    reserved_dates = get_reserved_dates()

    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save()
            return redirect('reservation')
        else:
            print(form.errors)
    else:
        form = ReservationForm()

    context = {
        'form': form,
        'reserved_dates': reserved_dates,
        'houses': houses,
    }
    return render(request, 'reservation/reservation.html', context)
