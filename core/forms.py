from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.widgets.TextInput, max_length=30)
    password = forms.CharField(widget=forms.widgets.PasswordInput, max_length=30)

    class Meta:
        fields = ['username', 'password']
