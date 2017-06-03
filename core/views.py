from collections import OrderedDict
from django.views.generic import FormView, TemplateView, CreateView
from django.contrib.auth import login
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden, QueryDict

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


class ListUsersView(CheckPermissionsMixin, TemplateView):

    template_name = "core/list.html"
    permissions = [Permission.Choices.watch_list, ]

    def get_context_data(self, **kwargs):
        ctx = super(ListUsersView, self).get_context_data(**kwargs)
        ctx['permission_values'] = [p[1] for p in Permission.Choices.values]

        all_users = User.objects.filter(is_active=True).values_list('id', 'name')
        all_users_book = OrderedDict()
        for u in all_users:
            u_id, u_name = u
            all_users_book[u_name] = {}
            all_users_book[u_name]['id'] = u_id

        permissions = (Permission.objects.order_by('user__id')
                                         .filter(user__is_active=True)
                                         .values_list('user__name', 'status'))
        for p in permissions:
            user_name, status = p
            all_users_book[user_name][status] = True

        ctx['users_list'] = all_users_book
        return ctx


class UserCreateView(CheckPermissionsMixin, CreateView):

    permissions = [Permission.Choices.create_user, ]
    form_class = RegistrationForm
    success_url = reverse_lazy('users_list')
    template_name = "core/registration.html"


def api_enter_point(request, pk):

    def _update_user(pk, qd):
        updated_user = User.objects.filter(pk=pk).first()
        permission_name = qd.get('permission_name', None)
        new_value = qd.get('new_value', None)
        if updated_user and permission_name and new_value:
            if new_value == 'False':
                updated_user.remove_permission(permission_name)
            else:
                updated_user.add_permission(permission_name)
        return {}

    def _watch_user(pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            user_info = {
                'name': user.name,
                'permissions': user.get_avaible_permissions()
            }
        else:
            user_info = {}
        return user_info

    def _delete_user(pk):
        del_user = User.objects.filter(pk=pk).first()
        if del_user:
            del_user.is_active = False
            del_user.save()
        return {}

    user = request.user
    if not user.is_authenticated:
        return HttpResponseForbidden()

    if request.method not in ['GET', 'PUT', 'DELETE']:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

    if request.method == "GET" and user.has_permission(Permission.Choices.watch_list):
        d = _watch_user(pk)
    elif request.method == "PUT" and user.has_permission(Permission.Choices.edit_user):
        qd = QueryDict(request.body.decode('utf8'))
        d = _update_user(pk, qd)
    elif request.method == "DELETE" and user.has_permission(Permission.Choices.del_user):
        d = _delete_user(pk)
    else:
        return HttpResponseForbidden()
    return JsonResponse(d)
