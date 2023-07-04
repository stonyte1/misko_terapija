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


# def reservation_form(request):
#     if request.method == 'POST':
#         form1 = ReservationForm(request.POST)
#         form2 = ClientForm(request.POST)

#         if form1.is_valid() and form2.is_valid():
#             reservation = form1.save(commit=False)
#             reservation.house = form1.cleaned_data['house']
#             reservation.save()

#             client = form2.save(commit=False)
#             client.reservation = reservation
#             client.save()

#             return redirect('reservation')
#         else:
#             print(form1.errors, form2.errors)
#     else:
#         form1 = ReservationForm()
#         form2 = ClientForm()

#     context = {
#         'form1': form1,
#         'form2': form2,
#     }
#     return render(request, 'reservation/reservation_form.html', context)

