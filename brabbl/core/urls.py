from rest_framework import routers
from django.conf.urls import url

from . import views

router = routers.SimpleRouter()
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'wordings', views.WordingViewSet, basename='wording')
router.register(r'notification_wording',
                views.NotificationWordingViewSet,
                basename='notification_wording')
router.register(r'discussion_list', views.DiscussionListViewSet, basename='discussion_list')
router.register(r'discussions', views.DiscussionViewSet, basename='discussion')
router.register(r'news', views.NewsNotificationViewSet, basename='news')
router.register(r'statements', views.StatementViewSet, basename='statement')
router.register(r'arguments', views.ArgumentViewSet, basename='argument')
router.register(r'flag', views.FlagAPIView, basename='flag')
router.register(r'associated_file_upload', views.AssociatedFileUploadViewSet, basename='associated_file_upload')
urlpatterns = router.urls
urlpatterns += (
    url(r'^translation/$', views.TranslationAPIView.as_view(),
        name='translation'),
    url(r'^customer/$', views.CustomerAPIView.as_view({'get': 'retrieve'}),
        name='customer'),
    url(r'^get_update_info/$', views.UpdateInfoAPIView.as_view(),
        name='get_update_info'),
    url(r'^statistics/$', views.CustomerStatisticsAPIView.as_view(), name='statistics'),
)
