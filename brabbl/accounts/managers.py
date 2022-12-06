from django.conf import settings
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core import signing
from django.db.models.query import QuerySet
from brabbl.utils import logger


class CustomerQuerySet(QuerySet):
    def customer_for(self, obj):
        try:
            return obj.customer
        except AttributeError:
            return None


class UserManager(DjangoUserManager):
    def get_token_for(self, user):
        return signing.dumps((user.email, user.id))

    def get_by_token(self, token):
        try:
            return self.get(id=signing.loads(
                token, max_age=settings.MAX_EMAIL_CONFIRMATION_DAYS * 24 * 60 * 60)[1])
        except (signing.BadSignature, IndexError):
            logger.warning('Invalid confirmation token: %s', token, exception=True)
            raise self.model.DoesNotExist()
