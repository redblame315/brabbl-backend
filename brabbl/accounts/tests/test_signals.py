from django.test import TestCase

from brabbl.accounts.models import User
from brabbl.accounts.tests import factories


class CustomerSignalTests(TestCase):
    def test_update_usernames_with_token(self):
        customer = factories.CustomerFactory.create()
        user = factories.UserFactory.create(customer=customer,
                                            username="test+token")
        new_token = "new_token"
        customer.embed_token = new_token
        customer.save()
        updated_user = User.objects.get(pk=user.pk)
        self.assertEqual(updated_user.username, "test+new_token")
