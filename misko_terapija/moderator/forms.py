from django import forms
from home.models import House

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ('name', 'main_image', 'image', 'guests', 'beds', 'content')
