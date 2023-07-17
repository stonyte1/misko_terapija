from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from home.models import House, Image
from gallery.models import Gallery
from reservation.models import Reservation
from .forms import HouseForm, LoginForm


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
    
class GalleryUpdateView(LoginRequiredMixin, generic.View):
    template_name = 'moderator/gallery_form.html'

    def get(self, request):
        images = Gallery.objects.all()
        return render(request, self.template_name, {'images': images})

    def post(self, request):
        images = request.FILES.getlist('images')
        image_ids = request.POST.getlist('image_ids')

        for image_id in image_ids:
            gallery = Gallery.objects.get(id=image_id)
            gallery.delete()

        for image in images:
            gallery = Gallery.objects.create(photo=image)
            
        return redirect('gallery')
    
class ReservationDeleteView(LoginRequiredMixin, generic.View):
    template_name = 'moderator/reservation_delete.html'

    def get(self, request):
        reservations = Reservation.objects.all()
        return render(request, self.template_name, {'reservations': reservations})

    def post(self, request):
        reservations_id = request.POST.getlist('reservation_ids')

        for reservation_id in reservations_id:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.delete()

            
        return redirect('gallery') 

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
    return redirect('login')