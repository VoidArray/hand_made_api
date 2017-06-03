from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from core.views import LoginView, ListUsersView, UserCreateView, api_enter_point

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', ListUsersView.as_view(), name='users_list'),
    url(r'^add_user/$', ListUsersView.as_view(), name='add_user'),
    url(r'login/$', LoginView.as_view(), name='login'),

    url(r'users/(?P<pk>\d+)', api_enter_point, name='users'),
    url(r'users/', UserCreateView.as_view(), name='create_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
