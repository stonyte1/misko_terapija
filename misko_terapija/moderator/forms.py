from django import forms
from home.views import House

class HouseForm(forms.Form):
    class Meta:
        model = House
        fields = ('name', 'main_image', 'image', 'guests', 'beds', 'content')
