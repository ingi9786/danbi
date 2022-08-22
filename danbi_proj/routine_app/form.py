from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Myuser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=_("You can log in by email later."), label="E-mail")
    user_name = forms.CharField(max_length=30, required=False, label="username")
    
    class Meta:
        model = Myuser
        fields = (
            "email",
            "user_name",
            "password1",
            "password2",
        )


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder": "email"}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={"placeholder": "password"}))

