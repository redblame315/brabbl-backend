from django.urls import reverse
from django.test import TestCase, RequestFactory
from django_webtest import WebTest

from . import factories
from brabbl.accounts.models import EmailGroup, EmailTemplate
from brabbl.accounts.tests import factories as account_factories
from brabbl.core.views import DiscussionViewSet, StatementViewSet, ArgumentViewSet
from brabbl.core import models


class HideDeleteTest(TestCase):
    def setUp(self):
        super().setUp()
        self.customer = factories.CustomerFactory()
        self.discussion = factories.ComplexDiscussionFactory.create(
            customer=self.customer)
        self.statement = factories.StatementFactory.create(discussion=self.discussion)
        self.argument = factories.ArgumentFactory.create(statement=self.statement)

        self.factory = RequestFactory()
        self.request = self.factory.get('/fake/url/')
        self.request.customer = self.customer

    def init_view(self, View):
        view = View()
        view.request = self.request
        return view

    def test_querysets_should_exclude_hidden(self):
        dview = self.init_view(DiscussionViewSet)
        tview = self.init_view(StatementViewSet)
        aview = self.init_view(ArgumentViewSet)
        self.assertEqual(dview.get_queryset().count(), 1)
        self.assertEqual(tview.get_queryset().count(), 1)
        self.assertEqual(aview.get_queryset().count(), 1)
        self.argument.delete()
        self.assertEqual(dview.get_queryset().count(), 1)
        self.assertEqual(tview.get_queryset().count(), 1)
        self.assertEqual(aview.get_queryset().count(), 0)
        self.statement.delete()
        self.assertEqual(dview.get_queryset().count(), 1)
        self.assertEqual(tview.get_queryset().count(), 0)
        self.assertEqual(aview.get_queryset().count(), 0)
        self.discussion.delete()
        self.assertEqual(dview.get_queryset().count(), 0)
        self.assertEqual(tview.get_queryset().count(), 0)
        self.assertEqual(aview.get_queryset().count(), 0)


class DuplicateObjectTest(WebTest):
    def setUp(self):
        self.user = account_factories.StaffFactory(username='admin')
        self.user.set_password('admin')
        self.user.save()
        self.client.login(username='admin', password='admin')
        self.wording = factories.WordingFactory(name='Test')
        factories.WordingValueFactory(wording=self.wording)

        self.notification_wording = factories.NotificationWordingFactory(name='Test')
        factories.NotificationWordingMessageFactory(property_model=self.notification_wording)
        factories.MarkdownWordingMessageFactory(property_model=self.notification_wording)

        self.emailgroup = account_factories.EmailGroupFactory(name='Test')
        account_factories.EmailTemplateFactory(email_group=self.emailgroup)

    def test_wording_duplicate(self):
        rows_count = models.Wording.objects.count()
        self.client.get(reverse('duplicate-object', kwargs={
            'model': 'wording',
            'pk': self.wording.pk
        }))

        new_obj = models.Wording.objects.last()
        self.assertEqual(rows_count + 1, len(models.Wording.objects.all()))
        self.assertEqual("{} New".format(self.wording.name), new_obj.name)
        self.assertEqual(self.wording.words.count(), new_obj.words.count())

    def test_notificationwording_duplicate(self):
        rows_count = models.NotificationWording.objects.count()
        self.client.get(reverse('duplicate-object', kwargs={
            'model': 'notificationwording',
            'pk': self.notification_wording.pk
        }))

        new_obj = models.NotificationWording.objects.last()
        self.assertEqual(rows_count + 1, len(models.NotificationWording.objects.all()))
        self.assertEqual("{} New".format(self.notification_wording.name), new_obj.name)
        # import / pdb
        # pdb.set_trace()
        self.assertEqual(self.notification_wording.model_properties.count(), new_obj.model_properties.count())
        self.assertEqual(self.notification_wording.model_markdown_properties.count(),
                         new_obj.model_markdown_properties.count())

    def test_emailgroup_duplicate(self):
        rows_count = EmailGroup.objects.count()
        self.client.get(reverse('duplicate-object', kwargs={
            'model': 'emailgroup',
            'pk': self.emailgroup.pk
        }))

        new_obj = EmailGroup.objects.last()
        self.assertEqual(rows_count + 1, len(EmailGroup.objects.all()))
        self.assertEqual("{} New".format(self.emailgroup.name), new_obj.name)
        self.assertEqual(self.emailgroup.emailtemplate_set.count(), new_obj.emailtemplate_set.count())


class MigrateAvailableWordingsForCustomerTest(WebTest):
    def setUp(self):
        self.user = account_factories.StaffFactory(username='admin')
        self.user.set_password('admin')
        self.user.save()
        self.customer = factories.CustomerFactory()
        self.client.login(username='admin', password='admin')
        self.wording = factories.WordingFactory(name='Test')
        factories.WordingValueFactory(wording=self.wording)
        self.discussion = factories.SimpleDiscussionFactory(customer=self.customer,
                                                            discussion_wording=self.wording)
        self.notification_wording = factories.NotificationWordingFactory(name='Test')
        factories.NotificationWordingMessageFactory(property_model=self.notification_wording)
        factories.MarkdownWordingMessageFactory(property_model=self.notification_wording)

        self.emailgroup = account_factories.EmailGroupFactory(name='Test')
        account_factories.EmailTemplateFactory(email_group=self.emailgroup)

    def test_migration_available_wording_for_customer_success(self):
        available_wordings_count = self.customer.available_wordings.count()
        self.client.get(reverse('migrate-customer-available-wordings'))
        self.assertEqual(available_wordings_count + 1, len(self.customer.available_wordings.all()))

    def test_two_migration_available_wordings_for_customer_does_not_duplicate_same_wording(self):
        available_wordings_count = self.customer.available_wordings.count()
        self.client.get(reverse('migrate-customer-available-wordings'))
        self.assertEqual(available_wordings_count + 1, len(self.customer.available_wordings.all()))
        self.client.get(reverse('migrate-customer-available-wordings'))
        self.assertEqual(available_wordings_count + 1, len(self.customer.available_wordings.all()))
