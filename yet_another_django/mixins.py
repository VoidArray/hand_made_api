from django.views.generic import View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden


class CheckPermissionsMixin(View):

    permissions = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        for p in self.permissions:
            if not request.user.has_permission(p):
                return HttpResponseForbidden()

        return super(CheckPermissionsMixin, self).dispatch(request, *args, **kwargs)
