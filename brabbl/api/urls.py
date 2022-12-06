from django.conf.urls import include, url

from brabbl.accounts import urls as accounts_urls, views
from brabbl.core import urls as core_urls

app_name = 'api'
urlpatterns = [
    url(r'^account/', include(accounts_urls)),
    url(r'^', include(core_urls)),
    url(r'^accounts/user-list-update/$', views.UserListAPIView.as_view(), name='user-list-update'),
    url(r'^version/$', views.VersionApiView.as_view(), name='version')
]
