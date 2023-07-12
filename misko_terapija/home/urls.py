from django.urls import path
from . import views

urlpatterns = [
    path('', views.HouseView.as_view(), name='home'),
]



