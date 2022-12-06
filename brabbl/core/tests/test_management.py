from datetime import datetime, timedelta

from django.core import mail
from django.test import TestCase

from brabbl.accounts.models import User
from brabbl.accounts.tests import factories
from brabbl.core.management.commands import delete_non_confirmed_users, non_confirmed_users_warning_letter


class ManagementCommandsTestCase(TestCase):
    def setUp(self):
        customer = factories.CustomerFactory.create()
        self.user = factories.UserFactory.create(customer=customer, is_confirmed=True)
        self.user.date_joined = self.user.date_joined - timedelta(days=7)
        self.user.save()
        self.non_confirmed_user = factories.UserFactory.create(customer=customer, is_confirmed=False)
        self.non_confirmed_user.date_joined = self.non_confirmed_user.date_joined - timedelta(days=7)
        self.non_confirmed_user.save()

    def test_users_warning_letter(self):
        mails = len(mail.outbox)
        non_confirmed_users_warning_letter.Command().handle()
        self.assertEqual(len(mail.outbox), mails + 1)

    def test_delete_active_user(self):
        delete_non_confirmed_users.Command().handle()
        self.assertEqual(User.objects.filter(pk=self.user.pk).count(), User.objects.count())
