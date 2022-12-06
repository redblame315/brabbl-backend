from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from brabbl.accounts.models import User
from brabbl.core.models import Argument
from brabbl.utils import rating


class Command(BaseCommand):
    help = 'Deletes all non confirmed users after 24 hours'

    def handle(self, *args, **options):
        time_threshold = timezone.now() - timedelta(hours=24)
        users = User.objects.filter(is_confirmed=False, date_joined__lt=time_threshold)
        argument_list = set()
        for user in users:
            argument_list |= set(user.rating_set.values_list('pk', flat=True))
        users.delete()
        for argument in Argument.objects.filter(pk__in=argument_list):
            rating.denormalize_argument_rating(argument)
