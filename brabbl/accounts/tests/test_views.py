from rest_framework.authtoken.models import Token
from rest_framework import status

from django.urls import reverse
from django.template.defaultfilters import urlencode
from django_webtest import WebTest

from . import factories
from ..models import User, Customer
from brabbl.accounts import models
from brabbl.core.tests.factories import WordingFactory


class PasswordResetViewTest(WebTest):
    def setUp(self):
        super().setUp()
        self.user = factories.UserFactory.create(is_active=False, customer=factories.CustomerFactory.create())
        self.url = reverse('reset-password', args=(self.user.unique_token,))

    def test_url_invalid_token(self):
        self.user.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<form')

    def test_url_valid_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def _password_reset(self, url=None):
        response = self.app.get(url or self.url)
        self.assertEqual(response.status_code, 200)

        form = response.form
        form['new_password1'] = 'NewPassword'
        form['new_password2'] = 'NewPassword'

        response = form.submit()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'successful')
        return response

    def test_password_reset(self):
        self._password_reset()
        user = User.objects.get(username=self.user.username)
        self.assertTrue(user.check_password('NewPassword'))

    def test_password_should_match(self):
        response = self.app.get(self.url)
        self.assertEqual(response.status_code, 200)

        form = response.form
        form['new_password1'] = 'NewPassword'
        form['new_password2'] = 'Invalid'
        response = form.submit()

        self.assertContains(response, '<form')

    def test_redirect(self):
        next_url = self.user.customer.allowed_domains.splitlines()[0]
        response = self._password_reset()
        self.assertContains(response, 'http-equiv="refresh"')
        self.assertContains(response, 'redirected')
        self.assertContains(response, next_url)

        next_url = 'http://example.com/article-5/'
        url = '{0}?next={1}'.format(self.url, urlencode(next_url))
        response = self._password_reset(url=url)
        self.assertContains(response, 'http-equiv="refresh"')
        self.assertContains(response, 'redirected')
        self.assertContains(response, next_url)


class UserListViewTest(WebTest):
    def setUp(self):
        self.customer = factories.CustomerFactory.create()
        self.user = factories.StaffFactory(username='admin', customer=self.customer)
        self.token = Token.objects.get_or_create(user=self.user)[0]
        self.user.save()
        self.client.login(username='admin', password='admin')
        self.url = reverse('user-list') + "?token=Token " + self.token.key

    def test_user_list(self):
        response = self.client.get(self.url)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DuplicateObjectTest(WebTest):
    def setUp(self):
        self.user = factories.StaffFactory(username='admin')
        self.user.set_password('admin')
        self.user.save()
        self.client.login(username='admin', password='admin')
        self.customer = factories.CustomerFactory(name='Test')
        self.group = factories.GroupFactory()
        self.wording = WordingFactory()

    def test_customer_duplicate(self):
        self.customer.user_groups.add(self.group)
        self.customer.available_wordings.add(self.wording)
        rows_count = models.Customer.objects.count()
        self.client.get(reverse('duplicate-object-accounts', kwargs={
            'model': 'customer',
            'pk': self.customer.pk
        }))

        new_obj = models.Customer.objects.last()
        self.assertEqual(rows_count + 1, len(models.Customer.objects.all()))
        self.assertEqual("{} New".format(self.customer.name), new_obj.name)
        self.assertEqual(self.customer.user_groups.count(), new_obj.user_groups.count())
        self.assertEqual(self.customer.available_wordings.count(), new_obj.available_wordings.count())
