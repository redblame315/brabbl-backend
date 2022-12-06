from django_rq import job
import requests
from requests import exceptions
from webpreview.excepts import WebpreviewException
from webpreview.previews import web_preview

from django.conf import settings


def image_exists(url):
    exists = False
    try:
        exists = requests.get(url).status_code == 200
    except (exceptions.MissingSchema, exceptions.ConnectionError):
        pass
    return exists


@job
def get_discussion_image(discussion, force=False):
    if (not discussion.image or discussion.image.size < 2000) and not image_exists(discussion.image_url):
        try:
            title, description, url = web_preview(discussion.source_url)
        except WebpreviewException:
            url = None
        else:
            if not url or not image_exists(url):
                protocol = "https" if settings.SESSION_COOKIE_SECURE else "http"
                url = "{}://{}/static/img/placeholder.png".format(
                    protocol, settings.SITE_DOMAIN
                )
            discussion.image_url = url
            discussion.save()
