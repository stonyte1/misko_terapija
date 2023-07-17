from django import forms
from home.models import House


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ('name', 'main_image', 'guests', 'beds', 'content')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
