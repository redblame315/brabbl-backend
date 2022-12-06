from datetime import datetime

from brabbl.utils.http import build_absolute_url
from django.db import models
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.files import get_thumbnailer


class TimestampedModelMixin(models.Model):
    created_at = models.DateTimeField(_("Creation date"), auto_now_add=True,
                                      editable=False)
    modified_at = models.DateTimeField(_("Modified date"), auto_now=True, editable=False)
    deleted_at = models.DateTimeField(_("Deletion date"), blank=True, null=True,
                                      editable=False)

    class Meta:
        abstract = True


class LastActivityMixin(models.Model):
    last_related_activity = models.DateTimeField(
        _("Last activity"), null=True, editable=False)

    @property
    def last_activity(self):
        if self.last_related_activity:
            return max([self.modified_at, self.last_related_activity])
        return self.modified_at

    class Meta:
        abstract = True


class SetOfPropertiesMixin(object):
    property_model = None

    def save(self, *args, **kwargs):
        super().save(**kwargs)
        properties = self.model_properties.all()
        SetOfPropertiesMixin.auto_create_delete_properties(self, properties, self.property_model)

    @staticmethod
    def auto_create_delete_properties(instance, properties, property_model):
        if len(property_model.FIELD_LIST) != properties.count():
            properties_for_create = []
            already_exist = list(map((lambda x: x.key), properties))
            fields = list(map((lambda x: x[0]), property_model.FIELD_LIST))
            properties.exclude(key__in=fields).all().delete()
            for field in fields:
                if field not in already_exist:
                    properties_for_create.append(property_model(
                        property_model=instance,
                        key=field,
                    ))
            if len(field) > 0:
                property_model.objects.bulk_create(properties_for_create)


def all_unexpired_sessions_for_user(user):
    user_sessions = []
    all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
    for session in all_sessions:
        session_data = session.get_decoded()
        if user.pk == int(session_data.get('_auth_user_id', 0)):
            user_sessions.append(session)
    return user_sessions


def delete_all_unexpired_sessions_for_user(user, session_to_omit=None):
    for session in all_unexpired_sessions_for_user(user):
        if session is not session_to_omit:
            session.delete()


def get_thumbnail_url(image, options):
    return build_absolute_url(
        get_thumbnailer(image).get_thumbnail(options).url)
