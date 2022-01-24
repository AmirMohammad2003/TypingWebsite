from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core import validators

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[validators.EmailValidator])

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
