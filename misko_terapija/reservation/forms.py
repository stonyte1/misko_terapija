from django import forms
from .models import Reservation, Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone_number')


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('date_from', 'date_to', 'house')
        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
            'date_to': forms.DateInput(attrs={'type': 'date'})
        }
