from typing import Any, Dict
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from home.models import House, Image
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