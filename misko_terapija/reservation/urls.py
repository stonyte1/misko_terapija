from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation, name='reservation'),
    # path('reserve/', views.reservation_form, name='reservation_form')
]
