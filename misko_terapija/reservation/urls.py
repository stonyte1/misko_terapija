from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_filter, name='reservation_filter'),
    path('<int:pk>/', views.reservation_create, name='house'),
]
