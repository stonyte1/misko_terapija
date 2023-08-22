from django.shortcuts import render
from .models import House, Review
from reservation.views import get_reserved_dates
from collections import Counter


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
    check_in_date = request.POST.get('check-in')
    check_out_date = request.POST.get('check-out')
    available_houses = None

    if request.method == 'POST':
        available_houses = []
        if check_in_date == '' or check_out_date == '':
            available_houses = None
        elif check_in_date and check_out_date:
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
        'check_in_date': check_in_date,  
        'check_out_date': check_out_date, 
    }
    return render(request, "home/home.html", context)
