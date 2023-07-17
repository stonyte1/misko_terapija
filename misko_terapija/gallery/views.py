from django.shortcuts import render
from .models import Gallery


def gallery(request):
    gallery = Gallery.objects.all()
    
    context = {
        'gallery': gallery
    }

    return render(request, 'gallery/gallery.html', context)