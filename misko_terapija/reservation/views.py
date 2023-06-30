from django.shortcuts import render, redirect
from .models import Reservation
from django.utils import timezone
from datetime import date, timedelta
from .forms import ReservationForm, ClientForm
from calendar import monthrange


def reservation_calendar(request):
    today = timezone.now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    month_name = date(year, month, 1).strftime('%B')
    weeks = []
    reservations = Reservation.objects.all()

    prev_month = date(year, month, 1) - timedelta(days=1)
    next_month = date(year, month, 1) + timedelta(days=32) 
    next_month = date(next_month.year, next_month.month, 1) if next_month.month != 1 else None

    for week_start in range(1, monthrange(year, month)[1] + 1, 7):
        week_end = min(week_start + 6, monthrange(year, month)[1])
        week = [(date(year, month, day), day) for day in range(week_start, week_end + 1)]
        weeks.append(week)

    context = {
        'month_name': month_name,
        'year': year,
        'weeks': weeks,
        'reservations': reservations,
        'prev_month': prev_month,
        'next_month': next_month,
        'weekdays': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    }

    return render(request, 'reservation/reservation.html', context)

def reservation_form(request):
    if request.method == 'POST':
        form1 = ReservationForm(request.POST)
        form2 = ClientForm(request.POST)
        
        if form1.is_valid() and form2.is_valid():
            reservation = form1.save()
            client = form2.save(commit=False)
            client.reservation = reservation
            client.save()
            return redirect('reservation') 
        else:
            print(form1.errors, form2.errors)
    else:
        form1 = ReservationForm()
        form2 = ClientForm()

    context = {
        'form1': form1,
        'form2': form2,
    }
    return render(request, 'reservation/reservation_form.html', context)
