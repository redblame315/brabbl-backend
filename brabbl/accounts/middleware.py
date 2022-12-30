from rest_framework.authtoken.models import Token
from rest_framework import exceptions

from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponseForbidden
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

from social_core.exceptions import SocialAuthBaseException
from social_core.utils import social_logger
from social_django.middleware import (
    SocialAuthExceptionMiddleware as SocialAuthExceptionBaseMiddleware
)

from brabbl.utils import logger, language_utils
from brabbl.accounts.models import Customer


class CustomerMiddleware(MiddlewareMixin):

    def process_request(self, request):
        host = request.META.get('HTTP_HOST', '')
        print(host)
        if '/auth/disconnect/' in request.path or '/auth/login/' in request.path:
            try:
                user = Token.objects.get(
                    key=request.META.get('HTTP_AUTHORIZATION', '').rsplit(' ')[-1]
                ).user
            except Exception:
                pass
            else:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

        if '/api/' not in request.path:
            return None

        if not request.META.get('HTTP_X_BRABBL_TOKEN'):
            return HttpResponseForbidden("Missing brabbl API Token.")

        try:
            request.customer = Customer.objects.get(
                embed_token=request.META['HTTP_X_BRABBL_TOKEN'])
            # set language for api by customer
            request = language_utils.set_language(
                request, request.customer.language
            )
        except Customer.DoesNotExist:
            return HttpResponseForbidden(_("Invalid brabbl API Token."))

        allowed_domains = request.customer.allowed_domains.splitlines()
        allowed_domains += [settings.SITE_DOMAIN, 'localhost:8000', '0.0.0.0:8000']

        referrer = request.META.get('HTTP_REFERER', '')
        try:
            referrer_domain = referrer.split('/', 3)[2]
        except IndexError:
            logger.info(
                _('Invalid referrer for customer %(customer)s: %(referrer)s'),
                customer=request.customer, referrer=referrer
            )
        else:
            if referrer_domain in allowed_domains:
                return None
            logger.info(
                _('Invalid referrer domain for customer %(customer)s: %(referrer)s'),
                customer=request.customer,
                referrer=referrer_domain
            )
            return HttpResponseForbidden(
                _("Invalid referrer domain for customer %(customer)s: %(referrer)s") % {'customer': request.customer,
                                                                                        'referrer': referrer_domain})


class AdminLocaleURLMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin'):
            request.LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG


class SocialAuthExceptionMiddleware(SocialAuthExceptionBaseMiddleware, MiddlewareMixin):
    def process_exception(self, request, exception):
        strategy = getattr(request, 'social_strategy', None)
        if request.user.is_authenticated and hasattr(request,
                                                     'customer') and request.customer != request.user.customer:
            logout(request)
        if strategy is None or self.raise_exception(request, exception):
            return

        if isinstance(exception, SocialAuthBaseException):
            backend = getattr(request, 'backend', None)
            backend_name = getattr(backend, 'name', 'unknown-backend')
            message = self.get_message(request, exception)
            social_logger.error(message)
            return redirect(request.session.get('back_url', ''))
