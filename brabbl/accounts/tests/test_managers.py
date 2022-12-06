from django.test import TestCase

from . import factories
from ..models import User


class UserManagerTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = factories.UserFactory.create()

    def test_unique_token(self):  # model test
        token = User.objects.get_token_for(self.user)
        self.assertEqual(self.user.unique_token, token)

    def test_get_by_token(self):
        token = User.objects.get_token_for(self.user)
        user = User.objects.get_by_token(token)
        self.assertEqual(user.id, self.user.id)
