from datetime import date

from django.test import TestCase

from . import factories
from brabbl.accounts.models import User, UserSocialAuth, Customer, DataPolicyAgreement


class SocialAuthMixinTestCase(TestCase):
    def test_get_social_auth(self):
        customer = factories.CustomerFactory.create()
        user = factories.UserFactory.create(customer=customer)
        self.assertIsNone(UserSocialAuth.get_social_auth('facebook', 123, customer))
        social_auth = UserSocialAuth.objects.create(
            user=user, customer=customer,
            provider='facebook', uid=123
        )
        self.assertEqual(
            social_auth,
            UserSocialAuth.get_social_auth('facebook', 123, customer)
        )

    def test_create_social_auth(self):
        customer = factories.CustomerFactory.create()
        user = factories.UserFactory.create(customer=customer)
        social_auth_count = UserSocialAuth.objects.count()
        UserSocialAuth.create_social_auth(user, 123, 'facebook')
        self.assertEqual(social_auth_count + 1, UserSocialAuth.objects.count())

    def test_username_max_length(self):
        max_length = UserSocialAuth.username_max_length()
        self.assertEqual(int, type(max_length))
        self.assertTrue(max_length > 0)

    def test_get_social_auth_for_user(self):
        customer = factories.CustomerFactory.create()
        user = factories.UserFactory.create(customer=customer)
        social_auth = UserSocialAuth.objects.create(
            user=user, customer=customer,
            provider='facebook', uid=123
        )
        result = UserSocialAuth.get_social_auth_for_user(
            user=user, provider='facebook', id=social_auth.pk)
        self.assertEqual(social_auth.pk, result[0].pk)


class UserModelTest(TestCase):

    def test_display_name(self):
        customer = factories.CustomerFactory.create(displayed_username=Customer.DISPLAY_USERNAME)
        user = factories.UserFactory.create(customer=customer)
        self.assertEqual(user.display_name, user.username)
        customer.displayed_username = Customer.DISPLAY_NAME_LAST_NAME
        customer.save()
        self.assertEqual(user.display_name, "%s %s" % (user.first_name, user.last_name))


class CustomerModelTest(TestCase):

    def test_invite_token_generate_and_decode(self):
        customer = factories.CustomerFactory.create(displayed_username=Customer.DISPLAY_USERNAME)
        email = 'test@mail.com'
        token = customer.get_invite_token_for('test@mail.com')
        info = customer.get_info_by_token(token)
        self.assertEqual(email, info[0])
        self.assertEqual(customer.id, info[1])
