from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.UserRetrieveUpdateAPIView.as_view(), name='user-profile'),
    url(r'^login/$', views.UserLoginAPIView.as_view(), name='user-login'),
    url(r'^logout/$', views.UserLogoutAPIView.as_view(), name='user-logout'),
    url(r'^register/$', views.UserCreateAPIView.as_view(), name='user-create'),
    url(r'^reset/$', views.PasswordResetAPIView.as_view(), name='user-reset-password'),
    url(r'^confirm-data-policy/$',
        views.ConfirmDataPolicyView.as_view(), name='user-confirm-data-policy'),
    url(r'^invite-participant/$', views.InviteParticipantAPIView.as_view(), name='invite-participant'),
    url(r'^user-list/$', views.UserListAPIView.as_view(), name='user-list'),
]
