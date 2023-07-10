from django.views import generic
from .models import House


class HouseListView(generic.ListView):
    model = House
    template_name = "home/home.html"
    context_object_name = 'houses'



