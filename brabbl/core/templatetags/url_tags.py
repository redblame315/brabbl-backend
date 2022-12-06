from django import template
from urllib.parse import urlparse

from brabbl.utils import http
from brabbl.utils.models import get_thumbnail_url

register = template.Library()


@register.simple_tag
def build_absolute_url(url):
    return http.build_absolute_url(url)


@register.simple_tag
def get_thumbnail(image, resolution='48x48'):
    width, height = map(int, resolution.split('x'))
    if not image:
        return ''
    options = {'size': (width, height), 'crop': True}
    return get_thumbnail_url(image, options)


@register.filter
def domain(url):
    return urlparse(url).hostname


@register.filter
def strip_http(url):
    if '//' in url:
        return url.split('//')[1]
    return url
