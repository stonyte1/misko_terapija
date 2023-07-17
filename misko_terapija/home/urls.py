from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_search, name='home'),
]



