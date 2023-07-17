from django.shortcuts import render
from .models import House, Review
from reservation.models import Reservation
from datetime import timedelta
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

def get_all_reserved_date(houses):
    all_reserved_dates = []
    for house in houses:
        reserved_dates = get_reserved_dates(house.id)
        all_reserved_dates.extend(reserved_dates)
    all_house_reserved = [item for item, count in Counter(all_reserved_dates).items() if count > 1]
    return all_house_reserved

def reservation_search(request):
    houses = House.objects.all()
    reviews = Review.objects.all()
    reserved_dates = get_all_reserved_date(houses)
    available_houses = None

    if request.method == 'POST':
        check_in_date = request.POST.get('check-in')
        check_out_date = request.POST.get('check-out')
        available_houses = []
        print(check_in_date)
        print(check_out_date)

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
        'reviews': reviews,
        'available_houses': available_houses,
    }
    return render(request, "home/home.html", context)

