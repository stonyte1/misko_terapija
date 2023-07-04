from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from home.models import House
from .forms import HouseForm


class HouseUpdateView(generic.UpdateView):
    model = House
    template_name = 'moderator/house_form.html'
    success_url = reverse_lazy('home')
    form_class = HouseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        house = self.get_object()
        context['house'] = house
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Add any additional form customization here if needed
        return form

