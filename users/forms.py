from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.urls import reverse_lazy

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class PasswordAltResetForm(forms.Form):
    email = forms.EmailField(
        label="Укажите вашу электронную почту",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )


class UserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
