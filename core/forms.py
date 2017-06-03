from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.widgets.TextInput, max_length=30)
    password = forms.CharField(widget=forms.widgets.PasswordInput, max_length=30)

    class Meta:
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput, label="name")
    password = forms.CharField(widget=forms.TextInput, label="Password")

    class Meta:
        model = User
        fields = ['name', 'password']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.is_active = True
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user