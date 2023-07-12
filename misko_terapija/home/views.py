from typing import Any, Dict
from django.views import generic
from .models import House, Review


class HouseView(generic.TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.all()
        context['reviews'] = Review.objects.all()
        return context


