from django.core import mail
from django.test import TestCase

from . import factories
from brabbl.accounts.models import User
from brabbl.accounts.admin import UserAdmin


class AccountsAdminTestCase(TestCase):
    def test_send_news_mail(self):
        factories.UserFactory.create(newsmail_schedule=1)
        factories.UserFactory.create(newsmail_schedule=7)
        factories.UserFactory.create(newsmail_schedule=0)
        qs = User.objects.all()
        UserAdmin.send_newsmail(None, None, qs)
        self.assertEqual(len(mail.outbox), 2)
