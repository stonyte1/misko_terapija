from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation, name='reservation'),
    path('<int:pk>/', views.reservation_create, name='house'),
]
