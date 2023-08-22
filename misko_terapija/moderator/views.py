from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from home.models import House, Image
from reservation.models import Client, Reservation
from .forms import HouseForm, LoginForm
from reservation.views import get_reserved_dates

class HouseUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = House
    template_name = 'moderator/house_form.html'
    success_url = reverse_lazy('home')
    form_class = HouseForm

    def form_valid(self, form):
        house = form.save(commit=False)

        images = self.request.FILES.getlist('images')
        for image in images:
            image_obj = Image.objects.create(photo=image, house=house)

        house.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

class ReservationUpdateView(LoginRequiredMixin, generic.View):
    template_name = 'moderator/reservation_delete.html'

    def get(self, request, pk):
        house = get_object_or_404(House, pk=pk)
        reserved_dates = get_reserved_dates(pk)
        clients = Client.objects.all()

        search_query = request.GET.get('search')
        date_from = request.GET.get('date-from')
        date_to = request.GET.get('date-to')

        if search_query:
            clients = clients.filter(name__icontains=search_query)
        if date_from and date_to:
            clients = clients.filter(reservation__date_from__gte=date_from, reservation__date_to__lte=date_to)

        return render(request, self.template_name, {
            'house': house,
            'clients': clients,
            'reserved_dates': reserved_dates,
        })
    
    def post(self, request, pk):
        action = request.POST.get('action')
        if action == 'add':
            check_in_date = request.POST.get('check-in')
            check_out_date = request.POST.get('check-out')
            reservation = Reservation(date_from=check_in_date, date_to=check_out_date, house_id=pk)
            reservation.save()

            client = Client(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone-number'),
            reservation=reservation)

            client.save()

        elif action == 'delete':
            clients_id = request.POST.getlist('client_ids')

            for client_id in clients_id:
                client = Client.objects.get(id=client_id)
                reservations = client.reservation
                reservations.delete()
                client.delete()

        return redirect('home') 



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'moderator/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
