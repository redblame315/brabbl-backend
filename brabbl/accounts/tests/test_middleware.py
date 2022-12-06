from django.urls import reverse
from django.utils.translation import ugettext as _
from rest_framework.test import APITestCase

from .factories import CustomerFactory


class MiddlewareTest(APITestCase):
    def test_non_api_call(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

    def test_without_customer(self):
        response = self.client.get(reverse('v1:user-profile'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content.decode("utf-8"), 'Missing brabbl API Token.')

    def test_invalid_customer(self):
        response = self.client.get(reverse('v1:user-profile'),
                                   HTTP_X_BRABBL_TOKEN='test')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content.decode("utf-8"), _('Invalid brabbl API Token.'))

    def test_valid_customer(self):
        customer = CustomerFactory.create()
        response = self.client.post(reverse('v1:user-profile'),
                                    HTTP_X_BRABBL_TOKEN=customer.embed_token)

        self.assertEqual(response.status_code, 401)  # no creden
        self.assertNotEqual(response.content.decode("utf-8"), _('Invalid brabbl API Token.'))
