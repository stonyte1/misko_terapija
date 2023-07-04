from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.HouseUpdateView.as_view(), name='house_form'),
]