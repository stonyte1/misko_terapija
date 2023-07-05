from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from home.models import House, Image
from .forms import HouseForm

class HouseUpdateView(generic.UpdateView):
    model = House
    template_name = 'moderator/house_form.html'
    success_url = reverse_lazy('home')
    form_class = HouseForm

    def form_valid(self, form):
        house = form.save(commit=False)
        house.save()

        images = self.request.FILES.getlist('images')
        for image in images:
            image_obj = Image.objects.create(photo=image)
            house.images.add(image_obj)

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

