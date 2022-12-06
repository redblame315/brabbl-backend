import pytest

from social.tests.strategy import TestStrategy
from social.utils import module_member
from social.backends.utils import load_backends
from social.tests.models import (
    User, TestUserSocialAuth, TestNonce, TestAssociation, TestCode
)
from social.tests.backends.test_facebook import FacebookOAuth2Test
from social.storage.base import BaseStorage

from django.db.utils import IntegrityError

from .factories import CustomerFactory


class UserSocialAuth(TestUserSocialAuth):

    def __init__(self, customer, user, provider, uid, extra_data=None):
        self.customer = customer
        super().__init__(
            user=user, provider=provider, uid=uid, extra_data=extra_data
        )

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        return cls(user=user, provider=provider, customer=1, uid=uid)

    @classmethod
    def get_social_auth(cls, provider, uid, customer):
        customer = 1
        soc_user = cls.cache_by_uid.get(uid)
        if soc_user and soc_user.provider == provider and soc_user.customer == customer:
            return soc_user

    @classmethod
    def username_max_length(cls):
        return 1024

    @classmethod
    def create_user(cls, username, email=None, customer=None, **extra_user_fields):
        return User(username=username, email=email, **extra_user_fields)


class TestStorage(BaseStorage):
    user = UserSocialAuth
    nonce = TestNonce
    association = TestAssociation
    code = TestCode

    @classmethod
    def is_integrity_error(cls, exception):
        return exception.__class__ is IntegrityError


class Strategy(TestStrategy):

    def get_pipeline(self):
        return self.setting(
            'PIPELINE', (
                'social.pipeline.social_auth.social_details',
                'social.pipeline.social_auth.social_uid',
                'social.pipeline.social_auth.auth_allowed',
                'brabbl.accounts.pipeline.social_user',
                'social.pipeline.user.get_username',
                'brabbl.accounts.pipeline.create_user',
                'brabbl.accounts.pipeline.associate_user',
                'brabbl.accounts.pipeline.load_extra_data',
                'social.pipeline.user.user_details',
            )
        )


class FacebookTestCase(FacebookOAuth2Test):

    def pipeline_settings(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_PIPELINE': (
                'social.pipeline.social_auth.social_details',
                'social.pipeline.social_auth.social_uid',
                'social.pipeline.social_auth.auth_allowed',
                'brabbl.accounts.pipeline.social_user',
                'social.pipeline.user.get_username',
                'brabbl.accounts.pipeline.create_user',
                'brabbl.accounts.pipeline.associate_user',
                'brabbl.accounts.pipeline.load_extra_data',
                'social.pipeline.user.user_details',
            )
        })

    @pytest.mark.django_db(transaction=True)
    def test_login(self):
        """
        test login on facebook
        """
        Backend = module_member(self.backend_path)
        self.strategy = Strategy(TestStorage)
        self.customer = CustomerFactory.create()
        self.expected_username += '+{}'.format(self.customer.embed_token)
        self.strategy.session_set('customer_token', self.customer.embed_token)
        self.backend = Backend(self.strategy, redirect_uri=self.complete_url)
        self.name = self.backend.name.upper().replace('-', '_')
        self.complete_url = self.strategy.build_absolute_uri(
            self.raw_complete_url.format(self.backend.name)
        )
        backends = (self.backend_path,
                    'social.tests.backends.test_broken.BrokenBackendAuth')
        self.strategy.set_settings({
            'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': backends
        })
        self.strategy.set_settings(self.extra_settings())
        # Force backends loading to trash PSA cache
        load_backends(backends, force_load=True)
        User.reset_cache()
        TestUserSocialAuth.reset_cache()
        TestNonce.reset_cache()
        TestAssociation.reset_cache()
        TestCode.reset_cache()

        self.do_login()

    def test_partial_pipeline(self):
        '''
        we don`t use partial pipelines
        '''
        pass
