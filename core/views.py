from django.views.generic import ListView, FormView
from django.contrib.auth import login
from django.http import JsonResponse

from .models import User, Permission
from .forms import LoginForm

from yet_another_django.mixins import CheckPermissionsMixin


class LoginView(FormView):

    template_name = "core/login.html"
    form_class = LoginForm
    model = User
    success_url = "/"

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)


class ListUsersView(CheckPermissionsMixin, ListView):

    model = User
    permissions = [Permission.Choices.watch_list, ]
