from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from brabbl.utils.string import add_widget_hashtag


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def build_absolute_url(url_or_field):
    if callable(getattr(url_or_field, 'open', None)):
        if not settings.LIVE:
            # if it has an `open()` method, assume it is a FieldFile
            # and open once so localdevstorage can do its magic
            try:
                url_or_field.open()
            except IOError:
                return ''
        url = url_or_field.url
    else:
        # it's a string
        url = url_or_field

    if '//' in url:
        return url

    return '%s://%s%s' % (
        'https' if settings.SESSION_COOKIE_SECURE else 'http',
        settings.SITE_DOMAIN,
        url,
    )


def get_next_url(next_url, user):
    val = URLValidator()
    try:
        val(next_url)
    except ValidationError:
        if user:
            next_url = user.customer.allowed_domains.splitlines()[0]

    return add_widget_hashtag(next_url)
