from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import timezone

from brabbl.accounts.models import User
from brabbl.utils import mail


class Command(BaseCommand):
    help = 'Sends warning mails to non confirmet users after 12 hours'

    def handle(self, *args, **options):
        time_threshold = timezone.now() - timedelta(hours=12)
        users = User.objects.filter(is_confirmed=False, date_joined__lt=time_threshold)
        protocol = "https" if settings.SESSION_COOKIE_SECURE else "http"
        domain_url = "{}://{}".format(
            protocol, settings.SITE_DOMAIN
        )
        for user in users:
            mail.send_template(
                user.email, user.customer, mail.TYPE_NON_ACTIVE_USER_WARNING,
                sender=user.customer.moderator_email, context={
                    'user': user,
                    'url': reverse(
                        'verify-registration', kwargs={'token': user.unique_token}
                    ),
                    'next': domain_url
                }
            )
