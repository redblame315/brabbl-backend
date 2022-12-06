from rest_framework import exceptions

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from django.utils.translation import ugettext_lazy as _


class BrabblTokenAuthentication(TokenAuthentication):
    model = Token

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related('user').get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        return token.user, token


class BrabblIFrameTokenAuthentication():
    def authenticate(self, request):
        auth = request.GET.get('token', '').split()

        if not auth or auth[0].lower() != 'token':
            return False

        if len(auth) == 1 or len(auth) > 2:
            return False

        token = auth[1]
        try:
            token = Token.objects.select_related('user').get(key=token)
        except Token.DoesNotExist:
            return False
        else:
            return token.user
