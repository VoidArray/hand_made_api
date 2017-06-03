from django.views.generic import ListView, FormView, CreateView
from django.contrib.auth import login
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseNotAllowed

from .models import User, Permission
from .forms import LoginForm, RegistrationForm

from yet_another_django.mixins import CheckPermissionsMixin


class LoginView(FormView):

    template_name = "core/login.html"
    form_class = LoginForm
    model = User
    success_url = reverse_lazy('users_list')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)


class ListUsersView(CheckPermissionsMixin, ListView):

    template_name = "core/list.html"
    model = User
    permissions = [Permission.Choices.watch_list, ]

    def get_context_data(self, **kwargs):
        ctx = super(ListUsersView, self).get_context_data(**kwargs)
        ctx['permission_values'] = [p[1] for p in Permission.Choices.values]

        permissions = Permission.objects.values_list('user__name', 'status')
        permission_book = {}
        for p in permissions:
            user_name = p[0]
            permission_name = p[1]
            if user_name not in permission_book:
                permission_book[user_name] = {}
            permission_book[user_name][permission_name] = True

        ctx['permission_book'] = permission_book
        return ctx


class UserCreateView(CheckPermissionsMixin, CreateView):

    permissions = [Permission.Choices.create_user, ]
    form_class = RegistrationForm
    success_url = reverse_lazy('users_list')
    template_name = "core/registration.html"


def api_enter_point(request, pk):

    def _update_user(pk):
        print(request)
        return {}

    def _watch_user(pk):
        user_info = {
            'name': pk.name,
            'permissions': pk.get_avaible_permissions()
        }
        return user_info

    def _delete_user(pk):
        del_user = User.objects.filter(pk=pk).first()
        if del_user:
            del_user.is_acitve = False
            del_user.save()
        return {}

    user = request.user

    if request.method == "GET" and user.has_permission(Permission.Choices.watch_list):
        d = _watch_user(pk)
    elif request.method == "PUT" and user.has_permission(Permission.Choices.edit_user):
        d = _update_user(pk)
    elif request.method == "PATCH" and user.has_permission(Permission.Choices.edit_user):
        d = _update_user(pk)
    elif request.method == "DELETE" and user.has_permission(Permission.Choices.del_user):
        d = _delete_user(pk)
    else:
        return HttpResponseNotAllowed()
    return JsonResponse(d)
