from django.shortcuts import redirect
from django.contrib.auth import logout

from rest_framework.authtoken.models import Token
from social_django.models import DjangoStorage
from social_django.strategy import DjangoStrategy

from brabbl.accounts.models import UserSocialAuth


class Storage(DjangoStorage):
    user = UserSocialAuth


class Strategy(DjangoStrategy):

    def partial_load(self, token):
        customer_token = self.request.session.get('customer_token', '')
        return partial_load(self, token, customer_token)

    def redirect(self, url):
        if not self.request.user.is_anonymous:
            user = self.request.user
            token, created = Token.objects.get_or_create(user=user)
            url = '{}#token={}'.format(
                self.session_get('back_url', ''), token.key
            )
            _backend = self.session_get('social_auth_last_login_backend', '')
            _state = self.session_get('{}_state'.format(_backend), '')
            logout(self.request)
            self.session_set('{}_state'.format(_backend), _state)
            self.session_set('social_auth_last_login_backend', _backend)
        return redirect(url)


def partial_load(strategy, token, customer_token):
    partial = strategy.storage.partial.load(token)

    if partial:
        args = partial.args
        kwargs = partial.kwargs.copy()
        user = kwargs.get('user')
        social = kwargs.get('social')

        social['customer'] = customer_token

        if isinstance(social, dict):
            kwargs['social'] = strategy.storage.user.get_social_auth(**social)

        if user:
            kwargs['user'] = strategy.storage.user.get_user(user)

        partial.args = [strategy.from_session_value(val) for val in args]
        partial.kwargs = dict((key, strategy.from_session_value(val))
                              for key, val in kwargs.items())
    return partial
