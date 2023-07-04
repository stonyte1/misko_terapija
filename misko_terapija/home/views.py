from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import House
from reservation.forms import ReservationForm
from reservation.views import get_reserved_dates


def reservation_create(request, pk):
    house = get_object_or_404(House, pk=pk)
    reserved_dates = get_reserved_dates()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.house = house
            reservation.save()
            print(request.POST)
            return redirect('reservation')
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



