from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')

    # first_name = forms.CharField(max_length=100)
    # last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

