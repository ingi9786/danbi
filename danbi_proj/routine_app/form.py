import re
from wsgiref.validate import validator
from django import forms
from django.core.exceptions import *
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Myuser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=_("You can log in by email later."), label="E-mail")
    user_name = forms.CharField(max_length=30, required=False, label="username")
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    
    class Meta:
        model = Myuser
        fields = (
            "email",
            "user_name",
            "password1",
            "password2",
        )
    
    def clean(self):
        pwd = self.cleaned_data['password1']
        pwd2 = self.cleaned_data['password2']
        print(len(pwd))
        if len(pwd) < 9:
             raise ValidationError(
                    _("Password must be at least 8 digits."),
                    code="password_validate_error",
                )
        if pwd != pwd2:
            raise ValidationError(
                    _("The passwords are not the same."),
                    code="password_validate_error",
                )
        regex = re.compile(r'(.*[a-z?=A-Z])(?=.*[0-9])(?=.*[\W\S_]).*')
        if re.match(regex, pwd) is None:
            raise ValidationError(
                _("It must contain at least one special and numeric character."),
                code="password_validate_error",
            )
        return self.cleaned_data


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder": "email"}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={"placeholder": "password"}))

