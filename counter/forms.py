from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    height = forms.FloatField(label='Height (in cm)', required=True)
    weight = forms.FloatField(label='Weight (in kg)', required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2' ,'height', 'weight']