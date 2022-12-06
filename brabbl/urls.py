from django.conf import settings
from django.conf.urls import include, url, static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required

from brabbl.accounts.views import (
    PasswordResetView, WelcomeView, UserListView
)
from brabbl.core.views import DuplicateObject, MigrateAvailableWordingsForCustomer
from brabbl.accounts.views import AccountDuplicateObject, VersionApiView
from brabbl.api import urls as api_urls

urlpatterns = [
    url(r'^api/v1/', include(api_urls, namespace='v1')),
    url(r'^admin/core/duplicate/(?P<model>[^/]+)/(?P<pk>[0-9]+)/',
        staff_member_required(DuplicateObject.as_view()),
        name="duplicate-object"),
    url(r'^admin/accounts/duplicate/(?P<model>[^/]+)/(?P<pk>[0-9]+)/',
        staff_member_required(AccountDuplicateObject.as_view()),
        name="duplicate-object-accounts"),
    url(r'^admin/core/migrate/customer-available-wordings',
        staff_member_required(MigrateAvailableWordingsForCustomer.as_view()),
        name="migrate-customer-available-wordings"),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/rq/', include('django_rq.urls')),
    url(r'^auth/', include('social_django.urls', namespace='social')),

    url(r'^accounts/verify/(?P<token>[^/]+)/$', WelcomeView.as_view(),
        name='verify-registration'),
    url(r'^accounts/reset/(?P<token>[^/]+)/$', PasswordResetView.as_view(),
        name='reset-password'),
    url(r'^accounts/user-list/$', UserListView.as_view(), name='user-list'),
    url(r'^welcome/$', WelcomeView.as_view(), name='welcome-account'),
    url(r'^test/$', TemplateView.as_view(template_name='whitelabel.html')),
    url(r'^embed\.(css|js)$', TemplateView.as_view(template_name='embed.js',
                                                   content_type='application/js'))
]
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += url(r'^rosetta/', include('rosetta.urls')),

if settings.DEBUG:
    urlpatterns += static.static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
