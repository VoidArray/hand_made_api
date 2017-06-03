from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from core.views import LoginView, ListUsersView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', ListUsersView.as_view(), name='users_list'),
    url(r'login$', LoginView.as_view(), name='login'),

    url(r'delete/(?P<pk>\d+)', LoginView.as_view(), name='del_user'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
