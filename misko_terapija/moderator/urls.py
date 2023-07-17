from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.HouseUpdateView.as_view(), name='house_form'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('gallery/', views.GalleryUpdateView.as_view(), name="gallery_update"),
    path('reservation/', views.ReservationDeleteView.as_view(), name="reservation_delete")
]