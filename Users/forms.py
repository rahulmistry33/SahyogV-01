from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField()
    email = forms.EmailField(required=True, max_length=60)
    phone_number = forms.CharField(required=True, max_length=13)
    home_address = forms.CharField(required=True)
    work_address = forms.CharField(required=True)
    emergency_contact_1 = forms.CharField(required=True, max_length=13)
    emergency_contact_2 = forms.CharField(required=True, max_length=13)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone_number',
            'home_address',
            'work_address',
            'emergency_contact_1',
            'emergency_contact_2'
        )
