from django.views.generic import ListView, FormView, View, UpdateView
from django.contrib.auth import login
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse

from .models import User, Permission
from .forms import LoginForm

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


class DeleteUserView(CheckPermissionsMixin, UpdateView):

    permissions = [Permission.Choices.del_user, ]
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return JsonResponse({'success': True}, safe=False)
