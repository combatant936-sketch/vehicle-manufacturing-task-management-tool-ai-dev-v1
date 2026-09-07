from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    """
    Custom login form that uses email as the username field.
    Extends Django's built-in AuthenticationForm so all authentication
    logic (rate limiting, error messages) is inherited for free.
    """

    username = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "placeholder": "you@example.com",
                "class": "form-control",
                "id": "id_email",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "••••••••",
                "class": "form-control",
                "id": "id_password",
            }
        ),
    )
